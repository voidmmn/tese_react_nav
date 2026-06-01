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
#   EXPERIMENTS="E3 0.5 true" bash rodar_experimentos.sh 1 180
#
# Matriz default (label  eta  enable_stay_alert):
#   E1  baseline (sem Stay Alert) · E2/E3/E4 = eta 0.3/0.5/0.8 · E5 = adverso
# OBS: E5 ainda usa o mesmo mundo de E3 — cenário adverso (múltiplas anomalias
#      simultâneas) precisa de um config próprio (TODO).
# ===========================================================================
# Nota: sem 'set -u' — o setup.bash do ROS usa variáveis não definidas
# (AMENT_TRACE_SETUP_FILES) e quebraria com nounset.
set -o pipefail
source /opt/ros/humble/setup.bash
source "$HOME/tese_ws/install/setup.bash"
export ROS_LOCALHOST_ONLY=1 IGN_IP=127.0.0.1 IGN_PARTITION=tese_sim
export QT_QPA_PLATFORM=offscreen

REPS=${1:-10}
MAX_RUN_S=${2:-420}
RESULTS="$HOME/tese_ws/results"
mkdir -p "$RESULTS"

# matriz default (pode ser sobrescrita via env EXPERIMENTS, uma linha por exp)
DEFAULT_MATRIX="E1 0.0 false
E2 0.3 true
E3 0.5 true
E4 0.8 true
E5 0.5 true"
MATRIX="${EXPERIMENTS:-$DEFAULT_MATRIX}"

NODES='ign gazebo|ign-gazebo|parameter_bridge|robot_state_publisher|ros_gz_sim|static_transform_publisher|amcl|map_server|controller_server|planner_server|bt_navigator|behavior_server|smoother_server|velocity_smoother|waypoint_follower|lifecycle_manager|component_container|bellman_node|stay_alert_node|mission_node|metrics_node|anomaly_simulator|ros2 launch tese'

cleanup() {
  pkill -9 -f "$NODES" 2>/dev/null
  pkill -9 -x ruby 2>/dev/null
  # segunda passada: nós órfãos por PID (sobrevivem ao pkill -f)
  ps -eo pid,comm | grep -iE 'ign|ruby|component|amcl|controller_se|planner_se|bt_navig|behavior|smoother|velocity|waypoint|lifecycle|bellman|stay_alert|mission_no|metrics|anomaly|robot_state|parameter_br|static_transf|map_server' \
    | grep -v grep | awk '{print $1}' | xargs -r kill -9 2>/dev/null
  rm -f /dev/shm/fastrtps_* /dev/shm/sem.fastrtps_* 2>/dev/null
  sleep 5
}

mission_complete() {
  [ "$(timeout 6 ros2 topic echo /mission/state --once 2>/dev/null | grep -oE 'COMPLETE' | head -1)" = "COMPLETE" ]
}

run_one() {
  local label=$1 eta=$2 sa=$3 rep=$4
  echo ">>> $(date +%H:%M:%S) $label rep $rep/$REPS (eta=$eta stay_alert=$sa)"
  cleanup
  ros2 launch tese_nav experimento.launch.py \
    run_label:="$label" eta:="$eta" enable_stay_alert:="$sa" headless:=true \
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
while read -r label eta sa; do
  [ -z "$label" ] && continue
  for r in $(seq 1 "$REPS"); do run_one "$label" "$eta" "$sa" "$r"; done
done <<< "$MATRIX"
echo "=== BATERIA COMPLETA — CSVs em $RESULTS ==="
ls -1 "$RESULTS"/metrics_*.csv 2>/dev/null | wc -l | xargs echo "total de CSVs:"
