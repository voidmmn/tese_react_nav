#!/usr/bin/env bash
#
# Sprint S1 — pós-instalação (SEM sudo). Rode como usuário normal APÓS
# 'sudo bash s1_install.sh':
#
#     bash ~/tese_ws/s1_postinstall.sh
#
# Faz: rosdep update, configura ~/.bashrc, builda o workspace tese_ws.
# Idempotente.
# Nota: sem 'set -u' — os scripts de setup do ROS usam variáveis não
# definidas (ex.: AMENT_TRACE_SETUP_FILES) e quebrariam com nounset.
set -eo pipefail

if [[ $EUID -eq 0 ]]; then
  echo "ERRO: NÃO rode como root/sudo — rode como usuário normal." >&2
  exit 1
fi

WS="$HOME/tese_ws"
BRC="$HOME/.bashrc"

add_line() {  # adiciona linha ao .bashrc só se ainda não existir
  grep -qxF "$1" "$BRC" 2>/dev/null || echo "$1" >> "$BRC"
}

echo ">>> [1/4] rosdep update"
rosdep update

echo ">>> [2/4] Configurando ~/.bashrc"
add_line "source /opt/ros/humble/setup.bash"
add_line "export TURTLEBOT3_MODEL=burger"
add_line "source $WS/install/setup.bash"

echo ">>> [3/4] rosdep install das dependências do workspace"
source /opt/ros/humble/setup.bash
cd "$WS"
rosdep install --from-paths src --ignore-src -r -y || \
  echo "    (aviso: rosdep install reportou pendências — verifique acima)"

echo ">>> [4/4] colcon build"
colcon build --symlink-install
source "$WS/install/setup.bash"

echo ""
echo ">>> S1 concluído. Validação rápida:"
echo "      ros2 pkg list | grep tese_nav"
echo "      ros2 launch tese_nav stay_alert.launch.py run_label:=E3"
echo "      ign gazebo   # abre a interface do Gazebo Fortress"
