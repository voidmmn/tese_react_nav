#!/usr/bin/env python3
"""Reconcilia TODOS os lancamentos registrados com as execucoes analisadas.

Para que o censo de execucoes se sustente, os lancamentos e as tentativas incluidas
precisam ser reconciliaveis por identificacao de bateria, motivo de exclusao e criterio. Este
script nao infere nada: conta o que existe no sistema de arquivos e classifica
cada diretorio por um mapa DECLARADO abaixo. O que nao casa com o mapa sai como
'nao classificado', nunca com um motivo inventado.

INVENTARIO INDIVIDUAL (15/11/2026): a auditoria da rodada 3 observou que um resumo
agregado de contagens nao substitui o inventario de cada lancamento. O script passa a
emitir TAMBEM `reconciliacao_lancamentos_individual.csv`, com uma linha por log de
lancamento encontrado, e a declarar explicitamente a lacuna dos lotes cujos logs nao
foram preservados -- que nao sao inferidos nem preenchidos por estimativa.

Uso: python3 gerar_reconciliacao.py [results_dir] > reconciliacao.csv
"""
import os, re, sys, csv, collections

# Mapa declarado: diretorio -> (origem, criterio de exclusao)
# As quatro entradas '_pre_*' sao mecanicas: rodar_bateria_blocos.sh:19 e
# run_bateria_noturna.sh:30 MOVEM o conteudo de results/ para ca antes de iniciar
# uma bateria nova. Nao sao baterias fracassadas: sao o estado anterior arquivado.
MAPA = {
 '_pre_bateria':      ('estado anterior arquivado pelo executor', 'substituido por bateria posterior'),
 '_pre_blocos':       ('estado anterior arquivado pelo executor', 'substituido por bateria posterior'),
 '_pre_noturna':      ('estado anterior arquivado pelo executor', 'substituido por bateria posterior'),
 '_pre_rerun_P0':     ('estado anterior arquivado pelo executor', 'substituido por reexecucao P0'),
 '_bateria_contaminada': ('bateria contaminada por no orfao entre execucoes',
                          'descartada integralmente: no sobrevivente invalida o isolamento'),
 '_bloco1_parcial':   ('bloco interrompido antes do fim', 'incompleto: bloco nao fecha as repeticoes'),
 '_noturna_parcial_ruim': ('bateria noturna parcial', 'descartada: bateria nao concluiu'),
 '_noite1_abortada_20261013': ('bateria noturna abortada', 'descartada: execucao abortada'),
 '_noturna_20260901': ('bateria noturna de 01/09/2026', 'substituida; logs nao preservados'),
 '_gate_reuso_20261013': ('ensaio de regressao do portao de reuso', 'ensaio de instrumento, nao da matriz'),
 '_decaimento_sim_invalido_20261114': (
   'verificacao do decaimento sob relogio simulado, primeira tentativa',
   'descartada: a referencia do decaimento nascia do relogio de parede e nao era '
   'resemeada ao receber tempo simulado, de modo que lambda nunca foi aplicado '
   '(lam=0/423). Defeito do instrumento, nao resultado'),
 '_smoke_20260901':   ('ensaio de fumaca', 'ensaio de fumaca, nao da matriz'),
 '_smoke_cm_v1_20261013': ('ensaio de fumaca', 'ensaio de fumaca, nao da matriz'),
 '_smoke_cm_v2_20261013': ('ensaio de fumaca', 'ensaio de fumaca, nao da matriz'),
 '_smoke_heu_20261013': ('ensaio de fumaca', 'ensaio de fumaca, nao da matriz'),
 '_smoke_kof_20261013': ('ensaio de fumaca', 'ensaio de fumaca, nao da matriz'),
}

# Rotulos da verificacao direcionada do decaimento (14/11/2026): ficam na raiz mas NAO
# pertencem a matriz das 320. Declarados separadamente.
R201 = re.compile(r'^(CM|E3|HEU)[ws]$')

def rotulo(nome):
    m = re.match(r'launch_(.+?)_r(\d+)\.log$', nome)
    if m: return m.group(1), m.group(2)
    m = re.match(r'metrics_(.+?)_\d{8}_\d{6}\.csv$', nome)
    if m: return m.group(1), ''
    return None, None

# Lotes cujos logs de lancamento NAO foram preservados. Declarado, nao inferido: para
# estes o inventario individual nao existe e a linha correspondente diz isso, em vez de
# sumir do arquivo ou de ser preenchida por estimativa a partir da contagem de CSVs.
SEM_LOGS_PRESERVADOS = {'_noturna_20260901'}


def main():
    res = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/tese_ws/results')
    w = csv.writer(sys.stdout)
    w.writerow(['bateria', 'conjunto', 'rotulo', 'lancamentos', 'csvs',
                'origem', 'criterio_de_exclusao'])
    resumo = collections.Counter()
    individual = []

    for d in ['.'] + sorted(x for x in os.listdir(res) if os.path.isdir(os.path.join(res, x))):
        base = os.path.join(res, d)
        logs, csvs = collections.Counter(), collections.Counter()
        for f in os.listdir(base):
            lab, _ = rotulo(f)
            if lab is None: continue
            (logs if f.startswith('launch_') else csvs)[lab] += 1
        # inventario individual: uma linha por log de lancamento deste diretorio
        for f in sorted(os.listdir(base)):
            m = re.match(r'launch_(.+?)_r(\d+)\.log$', f)
            if m:
                individual.append((d if d != '.' else '(raiz)', m.group(1),
                                   m.group(2), f))
        for lab in sorted(set(logs) | set(csvs)):
            if d == '.':
                if R201.match(lab):
                    conj, org, crit = ('verificacao do decaimento',
                                       'verificacao direcionada do decaimento (14/11/2026)',
                                       'nao pertence a matriz das 320; conjunto proprio')
                else:
                    conj, org, crit = ('analisado', 'bateria final', '---')
            else:
                conj = 'excluido'
                org, crit = MAPA.get(d, ('NAO CLASSIFICADO', 'NAO CLASSIFICADO'))
            w.writerow([d if d != '.' else '(raiz)', conj, lab,
                        logs[lab], csvs[lab], org, crit])
            resumo[conj] += logs[lab]

    # grava o inventario individual ao lado do agregado
    saida = os.path.join(res, 'reconciliacao_lancamentos_individual.csv')
    with open(saida, 'w', newline='', encoding='utf-8') as fh:
        wi = csv.writer(fh)
        wi.writerow(['bateria', 'conjunto', 'rotulo', 'repeticao',
                     'log_de_lancamento', 'origem', 'criterio_de_exclusao'])
        for bat, lab, rep, f in individual:
            if bat == '(raiz)':
                if R201.match(lab):
                    conj, org, crit = ('verificacao do decaimento',
                                       'verificacao direcionada do decaimento (14/11/2026)',
                                       'nao pertence a matriz das 320; conjunto proprio')
                else:
                    conj, org, crit = ('analisado', 'bateria final', '---')
            else:
                conj = 'excluido'
                org, crit = MAPA.get(bat, ('NAO CLASSIFICADO', 'NAO CLASSIFICADO'))
            wi.writerow([bat, conj, lab, rep, f, org, crit])
        # lacunas declaradas: lotes sem logs preservados
        for bat in sorted(SEM_LOGS_PRESERVADOS):
            org, crit = MAPA.get(bat, ('NAO CLASSIFICADO', 'NAO CLASSIFICADO'))
            wi.writerow([bat, 'excluido', '(indisponivel)', '(indisponivel)',
                         'LOGS NAO PRESERVADOS: inventario individual inexistente '
                         'para este lote', org, crit])
    print(f'inventario individual: {saida} ({len(individual)} lancamentos)',
          file=sys.stderr)
    for bat in sorted(SEM_LOGS_PRESERVADOS):
        print(f'  lacuna declarada: {bat} nao tem logs preservados; seus lancamentos '
              f'nao entram no inventario individual', file=sys.stderr)

    print('', file=sys.stderr)
    for k, v in sorted(resumo.items()):
        print(f'{k:22s} lancamentos={v}', file=sys.stderr)
    print(f'{"TOTAL":22s} lancamentos={sum(resumo.values())}', file=sys.stderr)

if __name__ == '__main__':
    main()
