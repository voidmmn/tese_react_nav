#!/usr/bin/env bash
#
# Sprint S1 — instalação do ambiente base da simulação da tese.
# Parte PRIVILEGIADA (repos, chaves, apt, rosdep init). Rode UMA vez:
#
#     sudo bash ~/tese_ws/s1_install.sh
#
# Depois, como usuário normal (sem sudo), rode os passos pós-instalação
# (rosdep update, .bashrc, colcon build) — ou deixe o assistente fazê-los.
#
# Idempotente: pode ser reexecutado com segurança.
# Alvo: Ubuntu 22.04 (jammy), arm64/amd64. ROS2 Humble + Gazebo Harmonic + Nav2.
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "ERRO: rode com sudo —  sudo bash $0" >&2
  exit 1
fi

ARCH="$(dpkg --print-architecture)"
. /etc/os-release
echo ">>> S1 install | arch=${ARCH} | codename=${UBUNTU_CODENAME} (${VERSION_CODENAME})"

# --------------------------------------------------------------------------- #
echo ">>> [1/5] Pré-requisitos e repositório universe"
apt-get update
apt-get install -y software-properties-common curl gnupg lsb-release
add-apt-repository -y universe

# --------------------------------------------------------------------------- #
echo ">>> [2/5] Repositório ROS2 (S1.1)"
install -d -m 0755 /usr/share/keyrings
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=${ARCH} signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
http://packages.ros.org/ros2/ubuntu ${UBUNTU_CODENAME} main" \
  > /etc/apt/sources.list.d/ros2.list

# --------------------------------------------------------------------------- #
echo ">>> [3/5] Repositório Gazebo / OSRF (S1.2)"
curl -sSL https://packages.osrfoundation.org/gazebo.gpg \
  -o /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=${ARCH} signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] \
http://packages.osrfoundation.org/gazebo/ubuntu-stable ${UBUNTU_CODENAME} main" \
  > /etc/apt/sources.list.d/gazebo-stable.list

apt-get update

# --------------------------------------------------------------------------- #
echo ">>> [4/5] Instalando ROS2 Humble + ferramentas + Gazebo + Nav2"
# NOTA: 'ros-humble-desktop' (não 'desktop-full', que é do ROS1).
# NOTA: 'turtlebot3-gazebo' NÃO existe no repo (só targeta Gazebo Classic).
#       No Harmonic, spawnamos o robô a partir de 'turtlebot3-description'
#       via ros_gz (tratado no S2).
apt-get install -y \
  ros-humble-desktop \
  python3-colcon-common-extensions \
  python3-rosdep \
  gz-harmonic \
  ros-humble-ros-gz \
  ros-humble-navigation2 \
  ros-humble-nav2-bringup \
  ros-humble-slam-toolbox \
  ros-humble-turtlebot3 \
  ros-humble-turtlebot3-description \
  ros-humble-turtlebot3-navigation2

# --------------------------------------------------------------------------- #
echo ">>> [5/5] rosdep init (precisa de root; 'update' roda como usuário depois)"
if [[ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]]; then
  rosdep init
else
  echo "    rosdep já inicializado — pulando."
fi

echo ""
echo ">>> S1 (parte privilegiada) concluído."
echo ">>> Agora, como usuário NORMAL (sem sudo), rode:"
echo "       bash ~/tese_ws/s1_postinstall.sh"
