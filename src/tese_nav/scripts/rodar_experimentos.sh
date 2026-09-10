#!/usr/bin/env bash
# ===========================================================================
# Bateria de experimentos E1–E5 (S6). Roda cada configuração N vezes, headless,
# salvando um CSV por execução em ~/tese_ws/results/ (via metrics_node).
#
# Uso:
#   bash rodar_experimentos.sh [REPS] [MAX_RUN_S]
#     REPS       repetições por experimento (default 10)
#     MAX_RUN_S  timeout por execução em segundos (default 420)
#
# Subconjunto/smoke (sobrescreve a matriz por variável de ambiente):
#   EXPERIMENTS="E3 0.5 true default" bash rodar_experimentos.sh 1 600
#
# Matriz default (label  eta  enable_stay_alert  scenario):
#   E1 baseline (sem Stay Alert) · E2/E3/E4 = eta 0.3/0.5/0.8 (cenário default)
#   E5 = mesmo eta de E3 mas cenário ADVERSO (5 anomalias em clusters + 2 perigos)
# ===========================================================================
# Nota: sem 'set -u' — o setup.bash do ROS usa variáveis não definidas
# (AMENT_TRACE_SETUP_FILES) e quebraria com nounset.
set -o pipefail
source /opt/ros/humble/setup.bash
source "$HOME/tese_ws/install/setup.bash"
export ROS_LOCALHOST_ONLY=1 IGN_IP=127.0.0.1 IGN_PARTITION=tese_sim
export QT_QPA_PLATFORM=offscreen

REPS=${1:-10}
# tempo de parede até COMPLETE ~= sa_delay(45s) + missão(~365s) ~= 410s; 600 dá folga
MAX_RUN_S=${2:-600}
RESULTS="$HOME/tese_ws/results"
mkdir -p "$RESULTS"

# matriz default (pode ser sobrescrita via env EXPERIMENTS, uma linha por exp)
# colunas: label  eta  enable_stay_alert  scenario  reactive  keepout  avoid  npos  nint
#   E1        baseline (só ronda Nav2, sem camada afetiva)
#   E0        ABLAÇÃO η=0 (Stay Alert ligado, termo de valor zerado)
#   E2/E3/E4  sweep de η {0.3,0.5,0.8} (análise numérica da Q-table)
#   E5        cenário ADVERSO (5 anomalias em clusters)
#   APF       baseline reativo de campo potencial (mesma ronda Nav2)
#   RHM/RHB   perigo SOBRE a rota: método (recuo+keepout=ablação c) vs baseline
#   N1/N2     ruído de percepção (moderado/alto)
#   CONF      conflito atração-repulsão co-localizado
#   KOa/KOb   §8 ablação causal do keepout: (a) keepout-só, (b) recuo-só
DEFAULT_MATRIX="E1 0.0 false default stay_alert false true 0.0 0.0
E0 0.0 true default stay_alert false true 0.0 0.0
E2 0.3 true default stay_alert false true 0.0 0.0
E3 0.5 true default stay_alert false true 0.0 0.0
E4 0.8 true default stay_alert false true 0.0 0.0
E5 0.5 true adverse stay_alert false true 0.0 0.0
APF 0.5 true default apf false true 0.0 0.0
RHM 0.5 true route_hazard stay_alert true true 0.0 0.0
RHB 0.0 false route_hazard stay_alert false true 0.0 0.0
N1 0.5 true default stay_alert false true 0.3 0.05
N2 0.5 true default stay_alert false true 0.6 0.10
CONF 0.5 true conflict stay_alert false true 0.0 0.0
KOa 0.5 true route_hazard stay_alert true false 0.0 0.0
KOb 0.5 true route_hazard stay_alert false true 0.0 0.0"
MATRIX="${EXPERIMENTS:-$DEFAULT_MATRIX}"

NODES='ign gazebo|ign-gazebo|parameter_bridge|robot_state_publisher|ros_gz_sim|static_transform_publisher|fake_scan_publisher|amcl|map_server|controller_server|planner_server|bt_navigator|behavior_server|smoother_server|velocity_smoother|waypoint_follower|lifecycle_manager|component_container|bellman_node|stay_alert_node|mission_node|metrics_node|anomaly_simulator|ros2 launch tese'

cleanup() {
  pkill -9 -f "$NODES" 2>/dev/null
  pkill -9 -x ruby 2>/dev/null
  # segunda passada: nós órfãos por PID (sobrevivem ao pkill -f)
  ps -eo pid,comm | grep -iE 'ign|ruby|component|amcl|controller_se|planner_se|bt_navig|behavior|smoother|velocity|waypoint|lifecycle|bellman|stay_alert|mission_no|metrics|anomaly|robot_state|parameter_br|static_transf|fake_scan|map_server' \
    | grep -v grep | awk '{print $1}' | xargs -r kill -9 2>/dev/null
  rm -f /dev/shm/fastrtps_* /dev/shm/sem.fastrtps_* 2>/dev/null
  sleep 5
}

mission_complete() {
  [ "$(timeout 6 ros2 topic echo /mission/state --once 2>/dev/null | grep -oE 'COMPLETE' | head -1)" = "COMPLETE" ]
}

run_one() {
  local label=$1 eta=$2 sa=$3 scen=$4 rep=$5 react=${6:-stay_alert}
  local keepout=${7:-false} avoid=${8:-true} npos=${9:-0.0} nint=${10:-0.0}
  echo ">>> $(date +%H:%M:%S) $label rep $rep/$REPS (eta=$eta sa=$sa scen=$scen react=$react keepout=$keepout avoid=$avoid noise=$npos/$nint seed=$rep)"
  cleanup
  # §8: publish_keepout/enable_reactive_avoid explícitos; §13: run_seed=rep
  # (semente por repetição -> realizações de ruído independentes + registro).
  ros2 launch tese_nav experimento.launch.py \
    run_label:="$label" eta:="$eta" enable_stay_alert:="$sa" scenario:="$scen" \
    reactive:="$react" publish_keepout:="$keepout" enable_reactive_avoid:="$avoid" \
    noise_pos:="$npos" noise_int:="$nint" run_seed:="$rep" \
    headless:=true \
    > "$RESULTS/launch_${label}_r${rep}.log" 2>&1 &
  local t=0
  while [ "$t" -lt "$MAX_RUN_S" ]; do
    sleep 10; t=$((t + 10))
    if mission_complete; then echo "    COMPLETE em ${t}s"; sleep 4; cleanup; return; fi
  done
  echo "    [timeout ${MAX_RUN_S}s] encerrando"
  cleanup
}

echo "=== BATERIA: REPS=$REPS MAX_RUN_S=$MAX_RUN_S ==="
while read -r label eta sa scen react keepout avoid npos nint; do
  [ -z "$label" ] && continue
  scen=${scen:-default}; react=${react:-stay_alert}
  keepout=${keepout:-false}; avoid=${avoid:-true}; npos=${npos:-0.0}; nint=${nint:-0.0}
  for r in $(seq 1 "$REPS"); do
    run_one "$label" "$eta" "$sa" "$scen" "$r" "$react" "$keepout" "$avoid" "$npos" "$nint"
  done
done <<< "$MATRIX"
echo "=== BATERIA COMPLETA — CSVs em $RESULTS ==="
ls -1 "$RESULTS"/metrics_*.csv 2>/dev/null | wc -l | xargs echo "total de CSVs:"
