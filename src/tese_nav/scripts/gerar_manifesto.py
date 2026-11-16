#!/usr/bin/env python3
"""
Gera o MANIFESTO DE EXECUCOES da tese: um registro por execucao analisada.

Motivacao (13/11/2026): os totais de execucao citados na tese vinham de contagens
independentes -- a introducao dizia vinte configuracoes, a matriz experimental listava
vinte e uma linhas, os dados em disco tinham trinta e dois rotulos e a secao de
validade falava de 160 tentativas, numero correto para a matriz do artigo e nao para a
desta tese. Este script passa a ser a fonte unica: a Tabela de censo e todos os `n`
das tabelas de resultado devem fechar com o que ele produz.

Entradas (nenhuma delas e modificada):
  results/metrics_<LABEL>_<AAAAMMDD>_<HHMMSS>.csv   metricas por execucao
  results/<bateria>.log                             logs de bateria (linhas '>>> ')

Saida:
  results/manifesto_execucoes.csv

Validade: distancia percorrida > 1 m. Uma execucao imovel e desfecho de
confiabilidade de inicializacao, nao resultado de navegacao.

Censura: o limite de execucao e de RELOGIO DE PAREDE (600 s). Uma execucao valida que
nao atingiu COMPLETE dentro da janela tem duracao censurada a direita -- o valor
registrado e o relogio de missao simulado no instante da interrupcao.

SELECAO DE CONJUNTO (15/11/2026): results/ guarda DOIS conjuntos na mesma raiz --
a matriz historica de 320 execucoes (32 rotulos) e a verificacao direcionada do
decaimento de 60 execucoes (6 rotulos, CMw/CMs/E3w/E3s/HEUw/HEUs, 14/11/2026).
Percorrer a raiz sem filtrar produzia 380 registros, e nao o manifesto historico de
320 que a tese declara. O conjunto passa a ser escolhido explicitamente e cada um
tem manifesto proprio; nao existe mais um modo que os misture por omissao.

Uso:  python3 src/tese_nav/scripts/gerar_manifesto.py [results_dir] [--conjunto X]
      --conjunto historico    (padrao) 32 rotulos da matriz  -> manifesto_execucoes.csv
      --conjunto verificacao  6 rotulos do lote de relogio   -> manifesto_verificacao_decaimento.csv
"""
import csv
import datetime
import glob
import os
import re
import sys
from collections import Counter

VALID_DIST_M = 1.0
LIMITE_PAREDE_S = 600

# Rotulos da verificacao direcionada do decaimento (14/11/2026). Declarados aqui, nao
# inferidos: o mesmo conjunto esta em gerar_reconciliacao.py, e os dois precisam
# concordar. Sufixo w = relogio de parede, s = relogio simulado.
ROTULOS_VERIFICACAO = frozenset(
    f'{b}{c}' for b in ('CM', 'E3', 'HEU') for c in ('w', 's'))

CONJUNTOS = {
    'historico':   ('manifesto_execucoes.csv',
                    'matriz historica (32 rotulos)'),
    'verificacao': ('manifesto_verificacao_decaimento.csv',
                    'verificacao do decaimento (6 rotulos)'),
}


_MESES = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
          'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}


def pertence(rotulo, conjunto):
    """True se `rotulo` pertence ao conjunto pedido. Sem terceira via: um rotulo
    esta na verificacao ou na matriz historica."""
    na_verificacao = rotulo in ROTULOS_VERIFICACAO
    return na_verificacao if conjunto == 'verificacao' else not na_verificacao


def ler_logs(results):
    """Extrai (inicio, rotulo, repeticao, cenario, desfecho, log) de cada lancamento.

    Devolve (runs, brutos): `runs` sao os lancamentos que puderam ser datados, usados
    para casar com os CSVs; `brutos` e a contagem de TODAS as linhas de lancamento,
    inclusive as de logs sem cabecalho de data (o ensaio piloto, p. ex.).
    """
    runs = []
    brutos = 0
    for lf in sorted(glob.glob(os.path.join(results, '*.log'))):
        if os.path.basename(lf).startswith('launch_'):
            continue
        data = None
        anterior = None   # ultimo horario visto neste log, para virada de dia
        for linha in open(lf, encoding='utf-8', errors='replace'):
            if linha.startswith('>>> '):
                brutos += 1
            m = re.search(r'(\d{4}-\d{2}-\d{2})', linha)
            if m and ('BLOCO' in linha or 'nicio' in linha or 'BATERIA' in linha):
                data = m.group(1)
                anterior = None
            else:
                # Cabecalho em formato TEXTUAL, usado pelos dois logs da
                # verificacao do relogio:
                #   === ... inicio Sat Nov 14 02:42:48 PM -03 2026 ===
                # Acrescentado em 16/11/2026: o padrao anterior so reconhecia
                # AAAA-MM-DD, de sorte que estes dois logs nao eram datados e as
                # 60 execucoes da verificacao saiam "nao_casado", com cenario,
                # semente, bateria e commit vazios e apenas seis run_id distintos.
                mt = re.search(
                    r'nicio\s+\w{3}\s+(\w{3})\s+(\d{1,2})\s+(\d{1,2}):(\d{2}):(\d{2})'
                    r'\s*(AM|PM)?\b.*?(\d{4})', linha)
                if mt and ('nicio' in linha):
                    mes, dia, hh, mm, ss, ampm, ano = mt.groups()
                    if mes in _MESES:
                        hh = int(hh)
                        if ampm == 'PM' and hh != 12:
                            hh += 12
                        elif ampm == 'AM' and hh == 12:
                            hh = 0
                        data = '%s-%02d-%02d' % (ano, _MESES[mes], int(dia))
                        anterior = None
            m = re.match(r'>>> (\d{2}):(\d{2}):(\d{2}) (\S+) rep (\d+)/', linha)
            if m and data:
                h, mi, s, rotulo, rep = m.groups()
                # Virada de meia-noite: o lote simulado comecou 22:36 de 14/11 e
                # terminou 02:11 de 15/11. Sem isto, as execucoes apos a meia-noite
                # ficariam datadas no dia anterior e nao casariam com os CSVs.
                agora = (int(h), int(mi), int(s))
                if anterior is not None and agora < anterior:
                    data = (datetime.datetime.fromisoformat(data)
                            + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
                anterior = agora
                cen = re.search(r'scen=(\S+)', linha)
                # o commit so existe nas baterias rodadas a partir de
                # 13/11/2026; nas anteriores o campo fica vazio, e vazio e o
                # registro honesto -- nao se infere commit por data.
                com = re.search(r'commit=(\S+)', linha)
                runs.append({
                    'inicio': datetime.datetime.fromisoformat(f'{data} {h}:{mi}:{s}'),
                    'rotulo': rotulo, 'rep': int(rep),
                    'cenario': cen.group(1) if cen else '',
                    'commit': com.group(1) if com else '',
                    'desfecho': None, 'log': os.path.basename(lf),
                })
            if runs and runs[-1]['desfecho'] is None:
                if 'COMPLETE em' in linha:
                    runs[-1]['desfecho'] = 'concluida'
                elif f'timeout {LIMITE_PAREDE_S}s' in linha:
                    runs[-1]['desfecho'] = 'interrompida_pelo_limite'
    runs.sort(key=lambda r: r['inicio'])
    return runs, brutos


def ler_metricas(caminho):
    vals = {}
    for row in csv.reader(open(caminho, encoding='utf-8', errors='replace')):
        if len(row) == 3 and row[1]:
            vals[row[1]] = row[2]
    return vals


def main(results, conjunto='historico'):
    arquivo_saida, descricao = CONJUNTOS[conjunto]
    runs, brutos = ler_logs(results)

    # Portao dos logs (15/11/2026). O DESFECHO de cada execucao (concluida x
    # interrompida pelo limite) sai dos logs de bateria, nao dos CSVs. Sem eles este
    # script preenchia 'nao_casado' e contava toda execucao valida como concluida:
    # num clone sem logs o censo saia 320/311/311/0 em vez de 320/311/302/9, numero
    # DIFERENTE do declarado na tese, e sem nenhum aviso. A censura nao pode ser
    # reconstruida pela simples ausencia de registro de conclusao.
    if not runs:
        sys.exit('ERRO: nenhum log de bateria legivel em %s.\n'
                 'O desfecho e a censura de cada execucao saem dos logs, nao dos CSVs. '
                 'Sem eles o censo NAO e regeneravel: o total de concluidas sairia '
                 'inflado e as censuradas sairiam em zero. Nenhum manifesto foi '
                 'escrito.' % results)
    linhas = []
    descartados = 0
    for f in sorted(glob.glob(os.path.join(results, 'metrics_*.csv'))):
        base = os.path.basename(f)
        m = re.match(r'metrics_(.+)_(\d{8})_(\d{6})\.csv$', base)
        if not m:
            continue
        rotulo, d, t = m.groups()
        if not pertence(rotulo, conjunto):
            descartados += 1
            continue
        quando = datetime.datetime.strptime(d + t, '%Y%m%d%H%M%S')
        vals = ler_metricas(f)
        dist = float(vals.get('distance_traveled_m', '0') or 0)
        valida = dist > VALID_DIST_M
        # casa com o lancamento mais recente anterior ao arquivo (janela de 20 min)
        cand = [r for r in runs
                if r['rotulo'] == rotulo and 0 <= (quando - r['inicio']).total_seconds() <= 1200]
        reg = cand[-1] if cand else None
        linhas.append({
            'run_id': f"{rotulo}-r{reg['rep']}" if reg else f'{rotulo}-?',
            'config': rotulo,
            'cenario': reg['cenario'] if reg else '',
            'semente': reg['rep'] if reg else '',
            'bateria': reg['log'] if reg else '',
            'commit': reg.get('commit', '') if reg else '',
            'inicio': quando.isoformat(sep=' '),
            'desfecho': (reg['desfecho'] or 'nao_registrado') if reg else 'nao_casado',
            'validade': 'valida' if valida else 'invalida',
            'motivo_exclusao': '' if valida else f'imovel (distancia <= {VALID_DIST_M} m)',
            'mission_duration_s': vals.get('mission_duration_s', ''),
            'duracao_censurada': 'sim' if (valida and reg and reg['desfecho'] ==
                                           'interrompida_pelo_limite') else 'nao',
            'distance_traveled_m': vals.get('distance_traveled_m', ''),
            'anomalies_unique': vals.get('anomalies_unique', ''),
            'arquivo_metricas': base,
        })
    if not linhas:
        sys.exit(f'ERRO: nenhuma execucao do conjunto "{conjunto}" ({descricao}) foi '
                 f'encontrada em {results}. O manifesto NAO foi escrito.')
    linhas.sort(key=lambda r: (r['config'], r['inicio']))
    saida = os.path.join(results, arquivo_saida)
    with open(saida, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(linhas[0].keys()))
        w.writeheader()
        w.writerows(linhas)

    c = Counter()
    for r in linhas:
        c['tentadas'] += 1
        c['validas' if r['validade'] == 'valida' else 'imoveis'] += 1
        if r['duracao_censurada'] == 'sim':
            c['censuradas'] += 1
    # Contagem por desfecho EXPLICITO. Ate 15/11/2026 a linha de concluidas era
    # calculada como validas menos censuradas, o que transforma desfecho
    # desconhecido em conclusao: uma execucao "nao_casado" nao foi censurada e
    # portanto entrava na conta das concluidas sem que nada a demonstrasse.
    # Agora so conta quem tem desfecho registrado, e o desconhecido aparece em
    # linha propria.
    por_desfecho = Counter(r['desfecho'] for r in linhas)
    # Separado por classe de validade: das 18 execucoes historicas com desfecho
    # "interrompida_pelo_limite", 9 sao validas e censuradas e 9 sao imoveis --
    # que tambem estouraram o limite, mas por nao terem saido do lugar. Somar as
    # duas sob "validas" confundiria as duas coisas.
    val = Counter(r['desfecho'] for r in linhas if r['validade'] == 'valida')
    imo = Counter(r['desfecho'] for r in linhas if r['validade'] != 'valida')
    desconhecidas = por_desfecho['nao_casado'] + por_desfecho['nao_registrado']
    print(f'conjunto: {conjunto} -- {descricao}')
    print(f'manifesto: {saida}')
    print(f'arquivos de metricas do outro conjunto, ignorados: {descartados}')
    print(f"pares configuracao-cenario: {len(set(r['config'] for r in linhas))}")
    print(f"execucoes tentadas: {c['tentadas']}")
    print(f"execucoes validas: {c['validas']}")
    print(f"  concluiram a missao: {val['concluida']}")
    print(f"  interrompidas pelo limite: {val['interrompida_pelo_limite']}"
          f"  (censuradas por duracao: {c['censuradas']})")
    if desconhecidas:
        print(f"  DESFECHO DESCONHECIDO: {desconhecidas}"
              f"  ({por_desfecho['nao_casado']} sem lancamento correspondente,"
              f" {por_desfecho['nao_registrado']} casadas sem desfecho no log)")
    print(f"execucoes imoveis: {c['imoveis']}"
          f"  (das quais interrompidas pelo limite:"
          f" {imo['interrompida_pelo_limite']})")
    print(f"lancamentos registrados nos logs de bateria: {brutos}"
          f"  ({len(runs)} datados; o excedente sobre as tentadas sao baterias"
          f" anteriores descartadas)")

    # Interrompe com erro, em vez de imprimir um censo que nao se sustenta.
    # O pacote completo nao tem desfecho desconhecido; se aparecer um, e defeito
    # de associacao entre CSV e log, e nao resultado.
    if desconhecidas:
        print(f'ERRO: {desconhecidas} execucoes sem desfecho registrado. O censo'
              f' acima NAO demonstra conclusao para elas: desfecho desconhecido'
              f' nao e conclusao. Corrija a associacao entre os CSVs e os logs'
              f' antes de publicar este manifesto.', file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    argv = sys.argv[1:]
    conj = 'historico'
    if '--conjunto' in argv:
        i = argv.index('--conjunto')
        if i + 1 >= len(argv) or argv[i + 1] not in CONJUNTOS:
            sys.exit('uso: --conjunto {' + '|'.join(CONJUNTOS) + '}')
        conj = argv[i + 1]
        del argv[i:i + 2]
    main(argv[0] if argv else
         os.path.join(os.path.dirname(__file__), '..', '..', '..', 'results'), conj)
