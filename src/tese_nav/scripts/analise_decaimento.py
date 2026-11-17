#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analise da verificacao do relogio do decaimento: Tabelas 18 e 19 da tese.
==========================================================================

Regenera, a partir dos arquivos publicados em results/, as duas tabelas da
Secao 6.13:

  Tabela 18 (tab:res-afericao)  afericao do estimador restrito contra a
                                contagem DIRETA das aplicacoes de lambda, nas
                                mesmas execucoes.
  Tabela 19 (tab:res-relogio)   efeito do relogio dentro de cada configuracao,
                                media +- desvio padrao e delta de Cliff.

POR QUE ESTE ARQUIVO EXISTE. Ate 15/11/2026 o repositorio publicava os dados e
o executor da bateria temporal, mas nao um analisador que regenerasse estas
duas tabelas. Quem conferisse tinha de deduzir as escolhas metodologicas a
partir dos valores publicados -- em particular as do estimador restrito, cuja
selecao de pares, piso de magnitude e tolerancia nao eram executaveis. Todos os
parametros abaixo sao explicitos e ajustaveis pela linha de comando.

AS DUAS FONTES, E POR QUE SAO DUAS

  Os CSVs de metricas (metrics_<ROTULO>_*.csv) trazem os desfechos por execucao
  e sustentam a Tabela 19.

  Os logs de lancamento (launch_<ROTULO>_r<N>.log) trazem duas coisas que os
  CSVs nao trazem: a instrumentacao direta do campo, na forma
  "lam=<aplicadas>/<chamadas> obs=<n> clk=<wall|sim>", e a serie de Phi
  amostrada a cada publicacao, com tres casas decimais. A primeira da a coluna
  "Direto" da Tabela 18; a segunda da a coluna "Estimador".

O ESTIMADOR RESTRITO, como definido na Secao 4.5.2

  A queda de Phi entre amostras NAO e contador inequivoco de aplicacoes de
  lambda: renovacao por observacao, retencao de maximo, saturacao e troca de
  canal alteram Phi sem decaimento. A contagem restringe-se, por isso, a pares
  consecutivos de um MESMO canal -- identificado aqui pelo sinal de Phi --
  compativeis com a ausencia de atualizacao concorrente:

    - acima de um piso de magnitude (--piso), onde as tres casas decimais do
      registro ainda resolvem a razao;
    - com razao igual a lambda dentro de uma tolerancia (--tolerancia), que e o
      par compativel com decaimento aplicado sem observacao; ou
    - com razao exatamente igual a 1, compativel com nenhum dos dois.

  Toda razao fora dessas duas e indicio de atualizacao concorrente, e o par e
  excluido. O criterio e de COMPATIBILIDADE e nao de identificacao: uma
  renovacao que devolva o canal ao valor anterior tambem produz razao 1.

  O FILTRO pode deixar de reconhecer aplicacoes e observa apenas um subconjunto
  dos pares. A fracao calculada nesse subconjunto NAO constitui limite garantido
  para a fracao global: nas tres configuracoes aferidas ela ficou ACIMA da fracao
  direta, produzindo periodo estimado menor. Convem distinguir quatro coisas que
  a redacao antiga confundia -- a contagem de aplicacoes reconhecidas no
  subconjunto, a fracao dentro do subconjunto, a fracao sobre todas as chamadas,
  e o periodo inferido a partir de uma delas. Limite inferior vale para a
  CONTAGEM; nao se converte em limite para a fracao global.

  periodo estimado = periodo nominal por chamada / fracao de pares que aplicam

AGREGACAO. Direto e por soma dos ultimos contadores de cada execucao do grupo,
e nao por media das razoes de cada execucao: os contadores sao cumulativos e as
execucoes tem duracoes distintas, de sorte que a media das razoes pesaria
igualmente execucoes de tamanhos diferentes. O estimador agrega os pares de
todas as execucoes do grupo pelo mesmo motivo.

Uso:
    python3 analise_decaimento.py <dir_results> [--piso 0.05] [--tolerancia 0.02]
                                  [--lambda 0.85] [--periodo-nominal 1.0]
                                  [--varredura] [--saida <dir>]
"""
import argparse
import csv
import glob
import os
import re
import sys

ROTULOS = {'CM': ('CMw', 'CMs'), 'E3': ('E3w', 'E3s'), 'HEU': ('HEUw', 'HEUs')}

DESFECHOS = [
    ('anomalies_unique',       'Anomalias inspecionadas', 2),
    ('investigation_time_s',   'Tempo em investigacao [s]', 2),
    ('min_hazard_distance_m',  'Afastamento minimo [m]', 2),
    ('hazard_avoidances',      'Recuos', 2),
    ('route_deviations',       'Desvios de rota', 2),
]


# ----------------------------------------------------------------- utilidades
def cliffs_delta(a, b):
    """Identica a de analise_estatistica.py, para nao divergir entre analises."""
    gt = sum(1 for x in b for y in a if x > y)
    lt = sum(1 for x in b for y in a if x < y)
    return (gt - lt) / (len(a) * len(b))


def media_dp(v):
    n = len(v)
    m = sum(v) / n
    if n < 2:
        return m, 0.0
    var = sum((x - m) ** 2 for x in v) / (n - 1)
    return m, var ** 0.5


def ultimo_valor(caminho, metrica):
    """Ultimo registro da metrica no CSV (os contadores sao cumulativos)."""
    achado = None
    with open(caminho, encoding='utf-8', errors='replace') as fh:
        for linha in csv.reader(fh):
            if len(linha) >= 3 and linha[1] == metrica:
                try:
                    achado = float(linha[2])
                except ValueError:
                    pass
    return achado


# ------------------------------------------------------- Tabela 19: desfechos
def tabela_desfechos(results):
    saida = []
    for cfg, (rw, rs) in ROTULOS.items():
        col = {}
        for rot in (rw, rs):
            arqs = sorted(glob.glob(os.path.join(results, 'metrics_%s_*.csv' % rot)))
            if not arqs:
                print('ERRO: nenhum CSV para o rotulo %s em %s' % (rot, results),
                      file=sys.stderr)
                sys.exit(1)
            col[rot] = arqs
        for metrica, rotulo, casas in DESFECHOS:
            a = [ultimo_valor(f, metrica) for f in col[rw]]
            b = [ultimo_valor(f, metrica) for f in col[rs]]
            if any(x is None for x in a + b):
                continue
            ma, da = media_dp(a)
            mb, db = media_dp(b)
            saida.append({
                'config': cfg, 'desfecho': rotulo,
                'n_parede': len(a), 'n_simulado': len(b),
                'media_parede': ma, 'dp_parede': da,
                'media_simulado': mb, 'dp_simulado': db,
                'delta_cliff': cliffs_delta(a, b), 'casas': casas,
            })
    return saida


# ---------------------------------- Tabela 18: contagem direta e estimador
_RE_LAM = re.compile(r'lam=(\d+)/(\d+)\s+obs=(\d+)\s+clk=(\w+)')
_RE_LINHA = re.compile(r'Phi=([+-]?\d+\.\d+).*?lam=(\d+)/(\d+)\s+obs=(\d+)')


def logs_do_rotulo(results, rotulo):
    return sorted(glob.glob(os.path.join(results, 'launch_%s_r*.log' % rotulo)),
                  key=lambda p: int(re.search(r'_r(\d+)\.log$', p).group(1)))


def serie_do_log(caminho):
    """(phi, aplicadas, chamadas, obs) de cada linha de instrumentacao, em ordem.

    INTERVALOS VAZIOS. A linha so e emitida quando |Phi| > 1e-3 (bellman_node.py),
    de sorte que a serie tem LACUNAS: duas linhas consecutivas do log podem estar
    separadas por chamadas da guarda que nao deixaram registro, justamente na
    cauda de baixa magnitude. O contador cumulativo de chamadas que cada linha
    carrega permite detectar a lacuna: o par e genuinamente consecutivo apenas
    quando as chamadas avancam de exatamente um.
    """
    serie = []
    for linha in open(caminho, encoding='utf-8', errors='replace'):
        m = _RE_LINHA.search(linha)
        if m:
            serie.append((float(m.group(1)), int(m.group(2)),
                          int(m.group(3)), int(m.group(4))))
    return serie


def contagem_direta(arqs):
    """Verdade de referencia: soma dos ULTIMOS contadores de cada execucao."""
    aplicadas = chamadas = 0
    relogios = set()
    for f in arqs:
        serie = serie_do_log(f)
        if not serie:
            continue
        aplicadas += serie[-1][1]
        chamadas += serie[-1][2]
        for linha in open(f, encoding='utf-8', errors='replace'):
            m = _RE_LAM.search(linha)
            if m:
                relogios.add(m.group(4))
    return aplicadas, chamadas, relogios


def estimador_restrito(arqs, piso, tolerancia, lam, exigir_consecutivo=False):
    """Pares de mesmo canal compativeis com ausencia de atualizacao concorrente.

    `exigir_consecutivo=False` reproduz o estimador COMO FOI APLICADO na Secao
    4.5.2: ele dispoe apenas da serie de Phi dos logs, sem contadores, e portanto
    toma como par qualquer duas linhas consecutivas. `True` exige que o par
    cubra exatamente uma chamada da guarda, usando os contadores -- o que isola
    o acerto do filtro de razao do efeito das lacunas, e que o estimador
    historico nao tinha como fazer.

    Devolve (admitidos, aplicam, atravessam, acertos, falso_aplica, falso_nao):
    os tres ultimos so tem sentido com os contadores, e comparam a decisao do
    filtro com o que o campo registrou de fato.
    """
    admitidos = aplicam = atravessam = 0
    acertos = falso_aplica = falso_nao = 0
    for f in arqs:
        serie = serie_do_log(f)
        for (p, ap, sp, _op), (q, aq, sq, _oq) in zip(serie, serie[1:]):
            if sq - sp != 1:
                atravessam += 1
                if exigir_consecutivo:
                    continue
            if p == 0.0 or q == 0.0:
                continue
            if (p > 0) != (q > 0):          # troca de canal: par excluido
                continue
            if abs(p) < piso:               # abaixo do piso as 3 casas nao resolvem
                continue
            razao = abs(q) / abs(p)
            verdade = aq - ap               # 1 = lambda aplicado de fato
            if abs(razao - lam) <= tolerancia:
                admitidos += 1
                aplicam += 1
                if verdade == 1:
                    acertos += 1
                else:
                    falso_aplica += 1
            elif q == p:                    # razao exatamente 1
                admitidos += 1
                if verdade == 0:
                    acertos += 1
                else:
                    falso_nao += 1
            # qualquer outra razao: atualizacao concorrente, par excluido
    return admitidos, aplicam, atravessam, acertos, falso_aplica, falso_nao


def tabela_afericao(results, piso, tolerancia, lam, periodo_nominal):
    """Tabela 18: estimador contra contagem direta, nas mesmas execucoes.

    O braco de relogio de PAREDE e o que se afere, porque e o comportamento
    historico cujo periodo realizado se quer medir.
    """
    saida = []
    for cfg, (rw, _rs) in ROTULOS.items():
        arqs = logs_do_rotulo(results, rw)
        if not arqs:
            print('ERRO: nenhum log launch_%s_r*.log em %s' % (rw, results),
                  file=sys.stderr)
            sys.exit(1)
        aplicadas, chamadas, relogios = contagem_direta(arqs)
        if aplicadas == 0:
            print('ERRO: contadores de decaimento ausentes em %s.'
                  ' Apenas a bateria de verificacao os tem.' % rw, file=sys.stderr)
            sys.exit(1)
        direto = periodo_nominal * chamadas / aplicadas

        linha = {'config': cfg, 'rotulo': rw, 'n_execucoes': len(arqs),
                 'relogio': ','.join(sorted(relogios)),
                 'aplicacoes_diretas': aplicadas, 'chamadas': chamadas,
                 'fracao_direta': aplicadas / chamadas,
                 'periodo_direto_s': direto}
        for sufixo, exigir in (('aplicado', False), ('consecutivo', True)):
            adm, apl, atr, ok, fa, fn = estimador_restrito(
                arqs, piso, tolerancia, lam, exigir_consecutivo=exigir)
            if adm == 0 or apl == 0:
                print('ERRO: nenhum par admitido em %s com piso=%.3f tol=%.3f'
                      % (rw, piso, tolerancia), file=sys.stderr)
                sys.exit(1)
            est = periodo_nominal * adm / apl
            linha['pares_%s' % sufixo] = adm
            linha['aplicam_%s' % sufixo] = apl
            linha['periodo_%s_s' % sufixo] = est
            linha['vies_%s' % sufixo] = est / direto - 1.0
            linha['acertos_%s' % sufixo] = ok
            linha['falso_aplica_%s' % sufixo] = fa
            linha['falso_nao_aplica_%s' % sufixo] = fn
            linha['pares_que_atravessam_lacuna'] = atr
        saida.append(linha)
    return saida


PISOS = (0.03, 0.05, 0.08, 0.10, 0.12)
TOLERANCIAS = (0.015, 0.02, 0.03, 0.04)


def varredura(results, lam, periodo_nominal):
    """Sensibilidade ao piso e a tolerancia, nos intervalos da nota da Secao 4.5.2."""
    linhas = []
    for cfg, (rw, _) in ROTULOS.items():
        arqs = logs_do_rotulo(results, rw)
        aplicadas, chamadas, _ = contagem_direta(arqs)
        direto = periodo_nominal * chamadas / aplicadas if aplicadas else float('nan')
        for piso in PISOS:
            for tol in TOLERANCIAS:
                r = {'config': cfg, 'piso': piso, 'tolerancia': tol,
                     'periodo_direto_s': direto}
                for sufixo, exigir in (('aplicado', False), ('consecutivo', True)):
                    adm, apl, _a, _o, _fa, _fn = estimador_restrito(
                        arqs, piso, tol, lam, exigir_consecutivo=exigir)
                    per = periodo_nominal * adm / apl if apl else float('nan')
                    r['pares_%s' % sufixo] = adm
                    r['periodo_%s_s' % sufixo] = per
                    r['vies_%s' % sufixo] = per / direto - 1.0
                linhas.append(r)
    return linhas


# ------------------------------------- modo historico: series sem contadores
#
# A matriz historica de 320 execucoes rodou ANTES de o campo passar a contar as
# aplicacoes de lambda diretamente. Os seus logs trazem a serie periodica de Phi,
# mas nenhum contador, de sorte que aqui nao ha verdade de referencia nem como
# detectar as lacunas da serie. O estimador e o mesmo; o que muda e o que se pode
# afirmar sobre ele.
#
# DUAS CAUTELAS, declaradas:
#
#   1. Sem contadores, um par de linhas consecutivas pode atravessar chamadas que
#      nao deixaram registro -- a linha so e emitida quando |Phi| > 1e-3.
#      CONDICIONAL, corrigido em 17/11/2026: sem atualizacoes concorrentes e
#      mantido o mesmo canal, multiplas aplicacoes produzem razao aproximadamente
#      lambda^k, que o filtro de razao exclui; a lacuna reduziria a amostra em vez
#      de contaminar a contagem. Isso descreve o caso de decaimento puro e NAO e
#      regra geral: uma observacao nova no intervalo, ou troca de canal, produz
#      razao qualquer, que pode cair dentro da tolerancia e ser admitida como se
#      fosse par consecutivo. No lote instrumentado, excluir os pares com lacuna
#      nao alterou a estimativa nas condicoes examinadas (19 pares de 1036 em CMw).
#      Esse resultado nao garante identificacao das lacunas no historico, onde nao
#      ha contador que as revele.
#
#   2. SO se leem as publicacoes periodicas do campo, isto e, as linhas do
#      bellman_node. As mensagens de transicao do stay_alert_node tambem imprimem
#      "Phi=", mas sao leituras pontuais nos instantes de mudanca de estado, fora
#      da sequencia periodica: incluí-las foi o defeito da analise original, e
#      deslocava o periodo estimado de CM de 1,52 para 1,59 s.

_RE_HIST = re.compile(r'bellman_node\]:\s*Phi=([+-]?\d+\.\d+)')


def serie_historica(caminho):
    """Serie periodica de Phi do bellman_node, sem contadores."""
    return [float(m.group(1)) for m in
            (_RE_HIST.search(l) for l in
             open(caminho, encoding='utf-8', errors='replace')) if m]


def estimador_historico(arqs, piso, tolerancia, lam):
    """Mesmo filtro do estimador restrito, sobre series sem contadores.

    Devolve (candidatos, admitidos, aplicam): `candidatos` e o total de pares
    consecutivos examinados, de que se deriva a fracao excluida pelo filtro.
    """
    candidatos = admitidos = aplicam = 0
    for f in arqs:
        serie = serie_historica(f)
        for p, q in zip(serie, serie[1:]):
            candidatos += 1
            if p == 0.0 or q == 0.0:
                continue
            if (p > 0) != (q > 0):
                continue
            if abs(p) < piso:
                continue
            razao = abs(q) / abs(p)
            if abs(razao - lam) <= tolerancia:
                admitidos += 1
                aplicam += 1
            elif q == p:
                admitidos += 1
    return candidatos, admitidos, aplicam


def rotulos_historicos(results):
    """Rotulos de launch_<ROT>_r<N>.log que nao sao da bateria de verificacao."""
    verificacao = {r for par in ROTULOS.values() for r in par}
    achados = {}
    for f in glob.glob(os.path.join(results, 'launch_*_r*.log')):
        m = re.match(r'launch_(.+)_r(\d+)\.log$', os.path.basename(f))
        if m and m.group(1) not in verificacao:
            achados.setdefault(m.group(1), []).append(f)
    for r in achados:
        achados[r].sort(key=lambda p: int(re.search(r'_r(\d+)\.log$', p).group(1)))
    return achados


MIN_PARES = 100


def tabela_historica(results, piso, tolerancia, lam, periodo_nominal):
    """Estimador braco a braco sobre a matriz historica."""
    com, sem = [], []
    for rot, arqs in sorted(rotulos_historicos(results).items()):
        cand, adm, apl = estimador_historico(arqs, piso, tolerancia, lam)
        amostras = sum(len(serie_historica(f)) for f in arqs)
        if amostras == 0:
            # O braco nao sobe o bellman_node: nao ha campo atrator, logo nao ha
            # decaimento a estimar. E o caso da patrulha fixa, da linha de base de
            # campo potencial e dos bracos Q-driven.
            sem.append({'config': rot, 'n_execucoes': len(arqs),
                        'amostras_phi': 0, 'pares_candidatos': 0,
                        'pares_admitidos': 0,
                        'motivo': 'sem bellman_node: o braco nao mantem campo atrator'})
            continue
        if adm < MIN_PARES or apl == 0:
            sem.append({'config': rot, 'n_execucoes': len(arqs),
                        'amostras_phi': amostras, 'pares_candidatos': cand,
                        'pares_admitidos': adm,
                        'motivo': 'menos de %d pares admitidos' % MIN_PARES})
            continue
        com.append({'config': rot, 'n_execucoes': len(arqs),
                    'amostras_phi': amostras, 'pares_candidatos': cand,
                    'pares_admitidos': adm, 'pares_que_aplicam': apl,
                    'fracao_admitidos': apl / adm,
                    'fracao_excluida': 1 - adm / cand,
                    'periodo_estimado_s': periodo_nominal * adm / apl})
    com.sort(key=lambda r: r['periodo_estimado_s'])
    return com, sem


def varredura_historica(results, lam, periodo_nominal, alvo='CM'):
    """Sensibilidade do estimador historico, no braco indicado."""
    arqs = rotulos_historicos(results).get(alvo, [])
    linhas = []
    for piso in PISOS:
        for tol in TOLERANCIAS:
            _c, adm, apl = estimador_historico(arqs, piso, tol, lam)
            if adm and apl:
                linhas.append({'config': alvo, 'piso': piso, 'tolerancia': tol,
                               'pares_admitidos': adm,
                               'periodo_estimado_s': periodo_nominal * adm / apl})
    return linhas


def imprime_historico(com, sem, varr, alvo='CM'):
    print('=' * 86)
    print('ESTIMADOR SOBRE A MATRIZ HISTORICA (sem contadores: sem verdade de referencia)')
    print('=' * 86)
    print('  As 320 execucoes anteriores rodaram antes da instrumentacao direta. Aqui o')
    print('  estimador nao pode ser aferido, e os seus valores NAO sao corrigidos pelo')
    print('  vies medido no lote de verificacao -- esse transporte, quando feito, fica')
    print('  declarado no texto como aproximacao.')
    print()
    print('%-9s %4s %9s %9s %9s %10s' % (
        'Config', 'exec', 'candidat.', 'admitidos', 'aplicam', 'periodo'))
    for r in com:
        print('%-9s %4d %9d %9d %9d %9.3fs' % (
            r['config'], r['n_execucoes'], r['pares_candidatos'],
            r['pares_admitidos'], r['pares_que_aplicam'], r['periodo_estimado_s']))
    if com:
        ps = [r['periodo_estimado_s'] for r in com]
        print()
        print('  %d configuracoes com estimativa; faixa %.3f a %.3f s (%s a %s)' % (
            len(com), min(ps), max(ps), com[0]['config'], com[-1]['config']))
        alvo_r = [r for r in com if r['config'] == alvo]
        if alvo_r:
            r = alvo_r[0]
            print('  %s: %d pares admitidos, %d aplicam (%.4f%%), periodo %.6f s,'
                  ' %.2f%% dos pares excluidos' % (
                      alvo, r['pares_admitidos'], r['pares_que_aplicam'],
                      100 * r['fracao_admitidos'], r['periodo_estimado_s'],
                      100 * r['fracao_excluida']))
    if sem:
        print()
        print('  SEM ESTIMATIVA (%d configuracoes):' % len(sem))
        for r in sem:
            print('    %-9s %s' % (r['config'], r['motivo']))
    if varr:
        ps = [r['periodo_estimado_s'] for r in varr]
        print()
        print('  VARREDURA EM %s (%d combinacoes de piso e tolerancia): %.3f a %.3f s'
              % (alvo, len(varr), min(ps), max(ps)))


# ------------------------------------------------------------------ impressao
def imprime(desf, afer, varr):
    print('=' * 86)
    print('TABELA 18 (tab:res-afericao) -- estimador restrito contra contagem direta')
    print('=' * 86)
    print('  "aplicado"    = estimador como aplicado na Secao 4.5.2: pares de linhas')
    print('                  consecutivas do log, sem deteccao de lacuna.')
    print('  "consecutivo" = o mesmo filtro, restrito aos pares que cobrem exatamente')
    print('                  uma chamada da guarda (lacunas descartadas).')
    print()
    print('%-5s %8s %11s %8s %13s %8s' % (
        'Cfg', 'Direto', 'Aplicado', 'Vies', 'Consecutivo', 'Vies'))
    for r in afer:
        print('%-5s %7.3fs %10.3fs %+7.1f%% %12.3fs %+7.1f%%' % (
            r['config'], r['periodo_direto_s'],
            r['periodo_aplicado_s'], 100 * r['vies_aplicado'],
            r['periodo_consecutivo_s'], 100 * r['vies_consecutivo']))
    print()
    print('%-5s %11s %10s %9s %9s %9s' % (
        'Cfg', 'Aplic.(dir)', 'Chamadas', 'Pares', 'Acertos', 'Lacunas'))
    for r in afer:
        print('%-5s %10.1f%% %10d %9d %8d/%-6d %7d' % (
            r['config'], 100 * r['fracao_direta'], r['chamadas'],
            r['pares_consecutivo'], r['acertos_consecutivo'],
            r['pares_consecutivo'], r['pares_que_atravessam_lacuna']))
    print()
    print('  O filtro de razao classifica os pares consecutivos quase sem erro, mas o')
    print('  periodo que dele resulta e menor que o direto: os pares ADMITIDOS')
    print('  apresentam fracao de aplicacoes maior que a global. O vies e de SELECAO e')
    print('  nao de classificacao, e aponta para periodo curto.')
    print()
    print('  Nao se atribui aqui esse vies ao piso de magnitude isoladamente. Ausencia')
    print('  de linha de instrumentacao nao e ausencia de aplicacao: nos intervalos de')
    print('  CMw que atravessam lacunas do log os contadores acumulam 206 chamadas e')
    print('  133 aplicacoes, taxa proxima da global. Separar a contribuicao de cada')
    print('  filtro exigiria analise que estes dados nao sustentam.')
    print()
    print('=' * 86)
    print('TABELA 19 (tab:res-relogio) -- efeito do relogio dentro de cada configuracao')
    print('=' * 86)
    print('%-5s %-26s %16s %16s %8s' % (
        'Cfg', 'Desfecho', 'Parede', 'Simulado', 'delta'))
    atual = None
    for r in desf:
        c = r['config'] if r['config'] != atual else ''
        atual = r['config']
        print('%-5s %-26s %8.2f+-%-6.2f %8.2f+-%-6.2f %+8.2f' % (
            c, r['desfecho'], r['media_parede'], r['dp_parede'],
            r['media_simulado'], r['dp_simulado'], r['delta_cliff']))
    if varr:
        print()
        print('VARREDURA DE SENSIBILIDADE (piso 0,03-0,12; tolerancia 0,015-0,04)')
        for cfg in dict.fromkeys(r['config'] for r in varr):
            rs = [r for r in varr if r['config'] == cfg]
            d = rs[0]['periodo_direto_s']
            for sufixo in ('aplicado', 'consecutivo'):
                ps = [r['periodo_%s_s' % sufixo] for r in rs]
                vs = [100 * r['vies_%s' % sufixo] for r in rs]
                sinal = ('TROCA DE SINAL' if min(vs) < 0 < max(vs)
                         else 'sempre negativo' if max(vs) < 0 else 'sempre positivo')
                print('  %-4s %-12s %.3f a %.3f s   vies %+.1f%% a %+.1f%%   %s'
                      % (cfg, sufixo, min(ps), max(ps), min(vs), max(vs), sinal))
            print('  %-4s %-12s %.3f s' % (cfg, 'direto', d))


def grava(saida, nome, linhas):
    if not linhas:
        return
    caminho = os.path.join(saida, nome)
    with open(caminho, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(linhas[0].keys()))
        w.writeheader()
        w.writerows(linhas)
    print('gravado: %s' % caminho)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('results', help='diretorio results/ do pacote de reproducao')
    ap.add_argument('--piso', type=float, default=0.05,
                    help='piso de magnitude de |Phi| para admitir o par (padrao 0.05)')
    ap.add_argument('--tolerancia', type=float, default=0.02,
                    help='tolerancia da razao em torno de lambda (padrao 0.02)')
    ap.add_argument('--lambda', dest='lam', type=float, default=0.85,
                    help='fator de decaimento (padrao 0.85)')
    ap.add_argument('--periodo-nominal', type=float, default=1.0,
                    help='segundos simulados nominais por chamada (padrao 1.0)')
    ap.add_argument('--varredura', action='store_true',
                    help='varre piso e tolerancia, como a nota da Secao 4.5.2')
    ap.add_argument('--historico', action='store_true',
                    help='analisa tambem a matriz historica de 320 execucoes, cujos '
                         'logs tem a serie de Phi mas nao os contadores')
    ap.add_argument('--alvo-historico', default='CM',
                    help='braco historico detalhado e varrido (padrao CM)')
    ap.add_argument('--saida', default=None, help='diretorio dos CSVs (padrao: results)')
    a = ap.parse_args()

    if not os.path.isdir(a.results):
        print('ERRO: %s nao e diretorio' % a.results, file=sys.stderr)
        sys.exit(1)
    saida = a.saida or a.results

    desf = tabela_desfechos(a.results)
    afer = tabela_afericao(a.results, a.piso, a.tolerancia, a.lam, a.periodo_nominal)
    varr = varredura(a.results, a.lam, a.periodo_nominal) if a.varredura else []

    imprime(desf, afer, varr)
    print()
    grava(saida, 'verificacao_relogio_desfechos.csv', desf)
    grava(saida, 'verificacao_relogio_afericao.csv', afer)
    if varr:
        grava(saida, 'verificacao_relogio_varredura.csv', varr)

    if a.historico:
        com, sem = tabela_historica(a.results, a.piso, a.tolerancia, a.lam,
                                    a.periodo_nominal)
        hvarr = (varredura_historica(a.results, a.lam, a.periodo_nominal,
                                     a.alvo_historico) if a.varredura else [])
        print()
        imprime_historico(com, sem, hvarr, a.alvo_historico)
        print()
        grava(saida, 'historico_estimador.csv', com)
        grava(saida, 'historico_sem_estimativa.csv', sem)
        if hvarr:
            grava(saida, 'historico_varredura.csv', hvarr)


if __name__ == '__main__':
    main()
