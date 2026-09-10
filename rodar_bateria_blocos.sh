#!/usr/bin/env bash
# ============================================================================
# Bateria COMPLETA em BLOCOS (um config por vez, limpeza profunda entre blocos).
# Motivação: rodar tudo numa tacada degrada o WSL/DDS após ~15 runs (spawn-fails,
# Nav2 não carrega nós). Cada config vira um bloco fresco de 10 runs.
#
# Uso: bash rodar_bateria_blocos.sh
# Log geral: results/bateria_blocos.log (via redirecionamento)
# ============================================================================
set -o pipefail
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH
WS="$HOME/tese_ws"
cd "$WS" || exit 1
REPS=${1:-10}
MAXS=${2:-600}

# arquiva CSVs/logs soltos na raiz antes de começar (mantém subpastas _*)
mkdir -p "$WS/results/_pre_blocos"
mv "$WS"/results/metrics_*.csv "$WS"/results/launch_*.log "$WS/results/_pre_blocos/" 2>/dev/null

deep_clean() {
  pkill -9 -f "ign gazebo|ign-gazebo|parameter_bridge|robot_state_publisher|ros_gz_sim|static_transform_publisher|fake_scan_publisher|amcl|map_server|controller_server|planner_server|bt_navigator|behavior_server|smoother_server|velocity_smoother|waypoint_follower|lifecycle_manager|component_container|bellman_node|stay_alert_node|apf_node|qdriven_node|mission_node|metrics_node|anomaly_simulator|ros2 launch tese" 2>/dev/null
  pkill -9 -x ruby 2>/dev/null
  ps -eo pid,comm | grep -iE 'ign|ruby|component|amcl|controller_se|planner_se|bt_navig|behavior|smoother|velocity|waypoint|lifecycle|bellman|stay_alert|apf_node|qdriven|mission_no|metrics|anomaly|robot_state|parameter_br|static_transf|fake_scan|map_server' \
    | grep -v grep | awk '{print $1}' | xargs -r kill -9 2>/dev/null
  rm -f /dev/shm/fastrtps_* /dev/shm/sem.fastrtps_* 2>/dev/null
  sleep 12
}

# BLOCOS: label eta stay_alert scenario reactive keepout avoid [npos nint]
run_block() {
  local label=$1 eta=$2 sa=$3 scen=$4 react=$5 keepout=${6:-false} avoid=${7:-true} npos=${8:-0.0} nint=${9:-0.0}
  echo "===== BLOCO $label ($(date '+%F %T')) ====="
  deep_clean
  EXPERIMENTS="$label $eta $sa $scen $react $keepout $avoid $npos $nint" \
    bash "$WS/src/tese_nav/scripts/rodar_experimentos.sh" "$REPS" "$MAXS"
  echo "===== FIM BLOCO $label ($(date '+%F %T')) ====="
}

echo "########## BATERIA EM BLOCOS: início $(date '+%F %T') ##########"
# MATRIZ COMPLETA (16 configs) gerada do zero, ordem: fix-críticos (§7/§8:
# conflito, segurança, ablações, ensaio dirigido) primeiro; ruído/APF por último.
# colunas: label eta stay_alert scenario reactive keepout avoid [npos nint]
run_block E3   0.5 true  default      stay_alert false true
run_block CONF 0.5 true  conflict     stay_alert false true
run_block RHM  0.5 true  route_hazard stay_alert true  true
run_block RHB  0.0 false route_hazard stay_alert false true
run_block KOa  0.5 true  route_hazard stay_alert true  false
run_block KOb  0.5 true  route_hazard stay_alert false true
run_block DHa  0.5 true  dyn_hazard   stay_alert true  true   # perigo durante investig.: recuo+keepout
run_block DHb  0.5 true  dyn_hazard   stay_alert true  false  # perigo durante investig.: keepout-só
run_block E1   0.0 false default      stay_alert false true
run_block E0   0.0 true  default      stay_alert false true
run_block E2   0.3 true  default      stay_alert false true
run_block E4   0.8 true  default      stay_alert false true
run_block E5   0.5 true  adverse      stay_alert false true
run_block APF  0.5 true  default      apf        false true
run_block N1   0.5 true  default      stay_alert false true 0.3 0.05
run_block N2   0.5 true  default      stay_alert false true 0.6 0.10
deep_clean
echo "########## BATERIA EM BLOCOS: fim $(date '+%F %T') ##########"
echo ">>> análise (distribution-free canônica)..."
python3 "$WS/src/tese_nav/scripts/analise_estatistica.py" "$WS/results" 2>/dev/null || \
  echo "[aviso] análise falhou; CSVs salvos"
