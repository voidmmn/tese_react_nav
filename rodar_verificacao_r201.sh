#!/usr/bin/env bash
# ===========================================================================
# verificacao do decaimento — verificacao direcionada do decaimento temporal (14/11/2026)
#
# Esta verificacao resolve duas pendencias: (i) medida validada do periodo de decaimento
# realizado, contando aplicacoes de lambda DIRETAMENTE e nao quedas de |Phi|, e
# (ii) evidencia sobre influencia DIFERENCIAL do defeito entre bracos, hoje
# apenas afirmada. Esta bateria nao refaz as 320 execucoes historicas: roda tres
# blocos sob os dois relogios, com rotulos proprios, preservando o conjunto
# anterior para comparacao.
#
#   CM   cenario de risco marginal: a janela de supressao vive do decaimento
#   E3   metodo proposto (saliencia + disparo por Phi): USA a memoria
#   HEU  heuristica (proximidade + disparo por alcance): NAO usa a memoria
#
# HEU e o controle: se o relogio alterar CM/E3 e nao alterar HEU, a influencia
# do defeito e diferencial e os contrastes que dependem da persistencia precisam
# ser condicionados.
#
# Uso: bash rodar_verificacao_r201.sh [REPS]
# ===========================================================================
set -o pipefail
REPS=${1:-10}
MAX_RUN_S=420
RUNNER="$HOME/tese_ws/src/tese_nav/scripts/rodar_experimentos.sh"
LOG="$HOME/tese_ws/results/verificacao_r201.log"

echo "=== verificacao do decaimento: verificacao direcionada | REPS=$REPS | inicio $(date) ===" | tee "$LOG"

for clk in wall sim; do
  suf=$([ "$clk" = wall ] && echo w || echo s)
  MATRIX="CM$suf 0.5 true conflict_marginal stay_alert false true 0.0 0.0 saliency phi
E3$suf 0.5 true default stay_alert false true 0.0 0.0 saliency phi
HEU$suf 0.5 true default stay_alert false true 0.0 0.0 nearest range"
  echo ">>> relogio=$clk  blocos=CM$suf,E3$suf,HEU$suf  $(date +%H:%M:%S)" | tee -a "$LOG"
  EXPERIMENTS="$MATRIX" DECAY_CLOCK="$clk" bash "$RUNNER" "$REPS" "$MAX_RUN_S" 2>&1 | tee -a "$LOG"
done

echo "=== verificacao do decaimento: fim $(date) ===" | tee -a "$LOG"
