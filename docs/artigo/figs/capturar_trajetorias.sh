#!/usr/bin/env bash
# Captura a trajetória (pose no frame map) de 1 run E1 e 1 run E3, p/ a figura.
# Não mistura com a bateria: remove os metrics_traj_* ao final.
set -o pipefail
source /opt/ros/humble/setup.bash
source "$HOME/tese_ws/install/setup.bash"
export ROS_LOCALHOST_ONLY=1 IGN_IP=127.0.0.1 IGN_PARTITION=tese_sim QT_QPA_PLATFORM=offscreen
WS="$HOME/tese_ws"; FIGS="$WS/docs/artigo/figs"; MAX=600

NODES='ign gazebo|parameter_bridge|robot_state_publisher|ros_gz_sim|static_transform_publisher|fake_scan_publisher|amcl|map_server|controller_server|planner_server|bt_navigator|behavior_server|smoother_server|velocity_smoother|waypoint_follower|lifecycle_manager|component_container|bellman_node|stay_alert_node|mission_node|metrics_node|anomaly_simulator|ros2 launch tese|pose_logger'
cleanup(){ pkill -9 -f "$NODES" 2>/dev/null; pkill -9 -x ruby 2>/dev/null;
  rm -f /dev/shm/fastrtps_* /dev/shm/sem.fastrtps_* 2>/dev/null; sleep 5; }

capture(){  # label eta sa scenario out.csv
  local label=$1 eta=$2 sa=$3 scen=$4 out=$5
  echo ">>> $(date +%T) capturando $label (eta=$eta sa=$sa $scen)"
  cleanup
  ros2 launch tese_nav experimento.launch.py run_label:="traj_$label" eta:="$eta" \
    enable_stay_alert:="$sa" scenario:="$scen" headless:=true \
    > "$FIGS/launch_traj_$label.log" 2>&1 &
  # espera Nav2 ativo (TF map->base disponível)
  local i; for i in $(seq 1 60); do
    grep -q "Managed nodes are active" "$FIGS/launch_traj_$label.log" 2>/dev/null && break
    sleep 2; done
  python3 "$FIGS/pose_logger.py" "$out" &   # começa a logar
  local lg=$!
  local t=0
  while [ "$t" -lt "$MAX" ]; do
    sleep 5; t=$((t+5))
    [ "$(timeout 6 ros2 topic echo /mission/state --once 2>/dev/null | grep -oE COMPLETE | head -1)" = COMPLETE ] && { echo "    COMPLETE em ${t}s"; break; }
  done
  kill -9 "$lg" 2>/dev/null
  cleanup
  echo "    -> $out ($(wc -l < "$out") pontos)"
}

capture E1 0.0 false default "$FIGS/traj_E1.csv"
capture E3 0.5 true  default "$FIGS/traj_E3.csv"
rm -f "$WS"/results/metrics_traj_*.csv 2>/dev/null   # não poluir a bateria
echo "=== captura concluída ==="
