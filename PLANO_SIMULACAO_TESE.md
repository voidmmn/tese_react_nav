# Plano de Implementação — Simulação para Tese de Doutorado
## Navegação Robótica Reativa Inteligente para Inspeção de Subestações

**Autor:** Prof. Milton Miranda Neto  
**Orientador:** Prof. Alexandre Cardoso (UFU)  
**Revista alvo:** IEEE Access (A2)  
**Data:** Maio/2026

---

## Visão Geral

Este plano descreve a implementação de um ambiente de simulação **independente** do projeto CGW Autopilot (GO2 PRO físico), com foco na coleta de resultados para o artigo. O pipeline é:

```
Gazebo Harmonic → ROS2 Humble → Nav2 → Bellman Atratora (Stay Alert) → Coleta de métricas
```

A validação segue três níveis:
1. **Simulação** — Gazebo Harmonic com modelo de subestação
2. **Hardware-in-the-loop** — GO2 PRO físico (se houver tempo)
3. **Campo real** — Subestação Axia, Araraquara (validação final)

---

## Pré-requisitos de ambiente

```
SO:          Ubuntu 22.04 LTS (Jammy)
ROS2:        Humble Hawksbill
Gazebo:      Harmonic (gz-harmonic)
Python:      3.10+
GPU:         Recomendado para Gazebo (NVIDIA ou AMD)
RAM:         Mínimo 16GB
```

> **Nota:** Use uma máquina separada do Jetson (notebook/desktop) para simulação.
> O Jetson permanece dedicado ao GO2 PRO físico.

---

## Sprint S1 — Ambiente base (Semana 1-2)

### S1.1 — Instalar ROS2 Humble

```bash
# Configurar repositórios
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Instalar ROS2 completo
sudo apt update
sudo apt install ros-humble-desktop-full -y
sudo apt install python3-colcon-common-extensions python3-rosdep -y

# Inicializar rosdep
sudo rosdep init && rosdep update

# Adicionar ao .bashrc
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### S1.2 — Instalar Gazebo Harmonic

```bash
# Adicionar repositório Gazebo
sudo curl https://packages.osrfoundation.org/gazebo.gpg \
  --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] \
  http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt update
sudo apt install gz-harmonic -y

# Bridge ROS2 ↔ Gazebo
sudo apt install ros-humble-ros-gz -y
```

### S1.3 — Instalar Nav2

```bash
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup -y
sudo apt install ros-humble-slam-toolbox -y  # para mapeamento futuro
```

### S1.4 — Criar workspace de simulação

```bash
mkdir -p ~/tese_ws/src
cd ~/tese_ws
colcon build
echo "source ~/tese_ws/install/setup.bash" >> ~/.bashrc
```

**Entregável S1:** ROS2 + Gazebo + Nav2 instalados e funcionando.  
**Validação:** `gz sim` abre interface gráfica. `ros2 topic list` funciona.

---

## Sprint S2 — Modelo do robô no Gazebo (Semana 2-3)

### S2.1 — Modelo do robô (diferencial simples)

Para o artigo, um robô diferencial simples é suficiente — evita a complexidade do modelo quadrúpede e foca no algoritmo de navegação.

```bash
sudo apt install ros-humble-turtlebot3-gazebo -y
sudo apt install ros-humble-turtlebot3-navigation2 -y
echo "export TURTLEBOT3_MODEL=burger" >> ~/.bashrc
source ~/.bashrc
```

> O TurtleBot3 é padrão para validação de algoritmos Nav2. A contribuição do artigo é o **algoritmo**, não o modelo do robô.

### S2.2 — Alternativa: modelo GO2 simplificado

Se necessário usar o GO2 no artigo, existe um modelo URDF disponível:

```bash
cd ~/tese_ws/src
git clone https://github.com/abizovnuralem/go2_ros2_support.git
cd ~/tese_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build
```

### S2.3 — Primeiro teste de navegação

```bash
# Terminal 1 — Gazebo com TurtleBot3
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# Terminal 2 — Nav2
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True

# Terminal 3 — RViz para visualização
ros2 launch nav2_bringup rviz_launch.py
```

**Entregável S2:** Robô simulado navegando em mundo simples com Nav2.

---

## Sprint S3 — Modelo da subestação (Semana 3-5)

### S3.1 — Estrutura do mundo Gazebo

Criar um modelo de subestação simplificado com os elementos relevantes para inspeção:

```
subestacao_world/
├── models/
│   ├── transformador/      # Transformador de potência
│   ├── disjuntor/          # Disjuntores
│   ├── barramento/         # Barramentos
│   ├── isolador/           # Isoladores
│   └── cerca/              # Cerca perimetral
├── worlds/
│   └── subestacao.sdf      # Mundo principal
└── launch/
    └── subestacao.launch.py
```

### S3.2 — Criar package ROS2 para a subestação

```bash
cd ~/tese_ws/src
ros2 pkg create --build-type ament_cmake subestacao_sim \
  --dependencies rclcpp std_msgs geometry_msgs
```

### S3.3 — Modelo SDF básico da subestação

```xml
<!-- subestacao.sdf — estrutura mínima -->
<sdf version="1.9">
  <world name="subestacao">
    <include><uri>model://sun</uri></include>
    <include><uri>model://ground_plane</uri></include>

    <!-- Cerca perimetral -->
    <model name="cerca_norte">
      <static>true</static>
      <pose>0 25 1 0 0 0</pose>
      <link name="link">
        <collision name="col">
          <geometry><box><size>50 0.2 2</size></box></geometry>
        </collision>
        <visual name="vis">
          <geometry><box><size>50 0.2 2</size></box></geometry>
        </visual>
      </link>
    </model>

    <!-- Transformador principal -->
    <model name="transformador_1">
      <static>true</static>
      <pose>10 10 0.75 0 0 0</pose>
      <link name="link">
        <collision name="col">
          <geometry><box><size>3 2 1.5</size></box></geometry>
        </collision>
        <visual name="vis">
          <geometry><box><size>3 2 1.5</size></box></geometry>
          <material><diffuse>0.3 0.3 0.8 1</diffuse></material>
        </visual>
      </link>
    </model>

    <!-- Adicionar mais equipamentos conforme necessário -->
  </world>
</sdf>
```

### S3.4 — Waypoints de inspeção (pontos de interesse)

Definir waypoints ao redor dos equipamentos críticos:

```python
# inspection_waypoints.yaml
waypoints:
  - name: "transformador_1_frente"
    x: 7.0
    y: 10.0
    yaw: 0.0
  - name: "transformador_1_lado"
    x: 10.0
    y: 7.0
    yaw: 1.57
  - name: "disjuntor_1"
    x: -5.0
    y: 5.0
    yaw: -1.57
  - name: "barramento_entrada"
    x: 0.0
    y: 0.0
    yaw: 0.0
```

**Entregável S3:** Mundo Gazebo com subestação simplificada e waypoints definidos.

---

## Sprint S4 — Navegação base com Nav2 (Semana 5-6)

### S4.1 — Configurar Nav2 para simulação

```yaml
# nav2_params_sim.yaml
bt_navigator:
  ros__parameters:
    use_sim_time: true
    global_frame: map
    robot_base_frame: base_link

controller_server:
  ros__parameters:
    use_sim_time: true
    controller_frequency: 20.0
    FollowPath:
      plugin: "nav2_mppi_controller::MPPIController"
      vx_max: 0.5
      wz_max: 1.0
      motion_model: "DiffDrive"

local_costmap:
  local_costmap:
    ros__parameters:
      use_sim_time: true
      global_frame: odom
      rolling_window: true
      width: 5
      height: 5
      resolution: 0.05

global_costmap:
  global_costmap:
    ros__parameters:
      use_sim_time: true
      global_frame: map
      resolution: 0.05
```

### S4.2 — Launch file de simulação completo

```python
# sim_navigation.launch.py
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Gazebo com subestação
        IncludeLaunchDescription('subestacao.launch.py'),
        # Nav2
        IncludeLaunchDescription('navigation2.launch.py',
            launch_arguments={'use_sim_time': 'true'}.items()),
        # Nó de missão
        Node(package='tese_nav', executable='mission_node'),
    ])
```

**Entregável S4:** Robô navegando entre waypoints da subestação no Gazebo.

---

## Sprint S5 — Implementação da Bellman Atratora (Semana 6-9)

### S5.1 — Arquitetura do Stay Alert

O módulo **Stay Alert** implementa o terceiro modo de missão — entre waypoints de inspeção, o robô executa navegação reativa guiada pela equação de Bellman modificada:

```
Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)] + η·Φ(s,a)

Onde:
  Q(s,a)  = valor Q padrão (Bellman)
  η       = peso do campo atrator (hiperparâmetro)
  Φ(s,a)  = função de atração baseada em eventos sensoriais
            Φ > 0: atração (anomalia detectada — aproximar)
            Φ < 0: repulsão (perigo — afastar)
            Φ = 0: comportamento neutro (Nav2 padrão)
```

### S5.2 — Estrutura do package tese_nav

```bash
cd ~/tese_ws/src
ros2 pkg create --build-type ament_python tese_nav \
  --dependencies rclpy std_msgs geometry_msgs nav2_msgs sensor_msgs
```

```
tese_nav/
├── tese_nav/
│   ├── bellman_node.py          # Equação de Bellman atratora
│   ├── stay_alert_node.py       # Modo Stay Alert
│   ├── anomaly_detector.py      # Detecção de anomalias (simulada)
│   ├── mission_node.py          # Gerenciador de missão (waypoints)
│   ├── metrics_node.py          # Coleta de métricas para artigo
│   └── utils/
│       ├── q_table.py           # Tabela Q
│       └── attraction_field.py  # Campo Φ(s,a)
├── config/
│   ├── nav2_params_sim.yaml
│   ├── waypoints.yaml
│   └── bellman_params.yaml
├── launch/
│   ├── simulation.launch.py
│   └── stay_alert.launch.py
└── worlds/
    └── subestacao.sdf
```

### S5.3 — bellman_node.py (esqueleto)

```python
"""
Bellman Atratora Node — Tese de Doutorado
==========================================
Implementa Q(s,a) com termo atrativo Phi(s,a).
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
import numpy as np

class BellmanNode(Node):

    def __init__(self):
        super().__init__('bellman_node')

        # Hiperparâmetros
        self.alpha  = 0.1    # taxa de aprendizado
        self.gamma  = 0.95   # fator de desconto
        self.eta    = 0.5    # peso do campo atrator

        # Tabela Q inicializada com zeros
        self.q_table = {}

        # Subscribers — fontes de anomalia (simuladas no Gazebo)
        self.create_subscription(Float64, '/anomaly/thermal',
                                 self._on_thermal, 10)
        self.create_subscription(Float64, '/anomaly/acoustic',
                                 self._on_acoustic, 10)

        # Publisher — modifica comportamento Nav2
        self.attraction_pub = self.create_publisher(
            Float64, '/stay_alert/attraction', 10)

        self.phi = 0.0  # campo atrator atual

    def _on_thermal(self, msg):
        """Ponto quente detectado — atrai o robô."""
        intensity = msg.data
        if intensity > 0.7:    # limiar de anomalia
            self.phi = intensity  # atração positiva
            self._publish_attraction()

    def _on_acoustic(self, msg):
        """Descarga parcial detectada — atrai o robô."""
        intensity = msg.data
        if intensity > 0.5:
            self.phi = intensity * 1.2  # descargas têm peso maior
            self._publish_attraction()

    def _update_q(self, state, action, reward, next_state):
        """Atualiza Q com termo de Bellman + atrator."""
        q_sa   = self.q_table.get((state, action), 0.0)
        q_next = max(self.q_table.get((next_state, a), 0.0)
                     for a in ['forward', 'left', 'right', 'stop'])

        # Equação de Bellman atratora
        td_error = reward + self.gamma * q_next - q_sa
        self.q_table[(state, action)] = (
            q_sa + self.alpha * td_error + self.eta * self.phi
        )

    def _publish_attraction(self):
        msg = Float64()
        msg.data = self.phi
        self.attraction_pub.publish(msg)
        self.get_logger().info(f'Phi(s,a) = {self.phi:.3f}')
```

### S5.4 — Fontes de anomalia simuladas no Gazebo

Para coleta de resultados sem hardware real, simular anomalias via plugins Gazebo:

```python
# anomaly_simulator.py — publica anomalias em pontos predefinidos
class AnomalySimulator(Node):
    def __init__(self):
        super().__init__('anomaly_simulator')
        self.thermal_pub  = self.create_publisher(Float64, '/anomaly/thermal', 10)
        self.acoustic_pub = self.create_publisher(Float64, '/anomaly/acoustic', 10)

        # Pontos de anomalia no mundo (posição x,y → intensidade)
        self.anomalies = {
            (10.0, 10.0): {'type': 'thermal',  'intensity': 0.85},
            (-5.0,  5.0): {'type': 'acoustic', 'intensity': 0.72},
            ( 0.0, 15.0): {'type': 'thermal',  'intensity': 0.91},
        }
        self.create_timer(0.5, self._check_proximity)
        self.robot_x = 0.0
        self.robot_y = 0.0
        self.create_subscription(Odometry, '/odom', self._on_odom, 10)

    def _check_proximity(self):
        for (ax, ay), props in self.anomalies.items():
            dist = ((self.robot_x - ax)**2 + (self.robot_y - ay)**2)**0.5
            if dist < 3.0:  # detecta anomalia a 3m
                intensity = props['intensity'] * (1 - dist/3.0)
                msg = Float64()
                msg.data = float(intensity)
                if props['type'] == 'thermal':
                    self.thermal_pub.publish(msg)
                else:
                    self.acoustic_pub.publish(msg)
```

**Entregável S5:** Robô executando Stay Alert — desvia da rota planejada para investigar anomalias simuladas.

---

## Sprint S6 — Coleta de métricas (Semana 9-11)

### S6.1 — Métricas para o artigo IEEE Access

| Métrica | Descrição | Como medir |
|---|---|---|
| Taxa de detecção | % anomalias encontradas/total | Contador em `metrics_node.py` |
| Tempo de missão | Tempo total para cobrir todos WPs | Timer ROS2 |
| Distância percorrida | Metros totais na missão | Integração odometria |
| Desvios de rota | Quantas vezes Φ > limiar | Contador em `bellman_node.py` |
| Tempo de investigação | Tempo gasto em cada anomalia | Timer por evento |
| Convergência Q | Evolução de Q(s,a) ao longo do tempo | Log da tabela Q |
| Comparativo | Stay Alert vs ronda simples (baseline) | Executar ambos |

### S6.2 — metrics_node.py

```python
class MetricsNode(Node):
    def __init__(self):
        super().__init__('metrics_node')
        self.metrics = {
            'anomalies_detected': 0,
            'anomalies_total': 3,         # do anomaly_simulator
            'mission_start': None,
            'mission_end': None,
            'distance_traveled': 0.0,
            'route_deviations': 0,
            'q_convergence': [],
        }
        self._log_file = open(f'metrics_{datetime.now():%Y%m%d_%H%M%S}.csv', 'w')
        self._log_file.write('timestamp,metric,value\n')
        self.create_timer(1.0, self._save_metrics)

    def _save_metrics(self):
        t = self.get_clock().now().nanoseconds / 1e9
        for k, v in self.metrics.items():
            if isinstance(v, (int, float)):
                self._log_file.write(f'{t},{k},{v}\n')
        self._log_file.flush()
```

### S6.3 — Experimentos planejados

| Experimento | Configuração | Repetições | Objetivo |
|---|---|---|---|
| E1 — Baseline | Ronda simples Nav2 sem Stay Alert | 10 | Referência |
| E2 — Stay Alert η=0.3 | Bellman com atração fraca | 10 | Efeito suave |
| E3 — Stay Alert η=0.5 | Bellman com atração média | 10 | Configuração proposta |
| E4 — Stay Alert η=0.8 | Bellman com atração forte | 10 | Limite superior |
| E5 — Cenário adverso | Múltiplas anomalias simultâneas | 10 | Robustez |

**Total:** 50 execuções (~30 min cada) = ~25h de simulação.

### S6.4 — Análise estatística

```python
# análise_resultados.py
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

# Carregar resultados
df_e1 = pd.read_csv('resultados_E1.csv')
df_e3 = pd.read_csv('resultados_E3.csv')

# Teste t de Student — comparar E1 vs E3
t_stat, p_value = stats.ttest_ind(
    df_e1['anomalies_detected'],
    df_e3['anomalies_detected']
)
print(f't={t_stat:.3f}, p={p_value:.4f}')

# Gráfico comparativo
plt.boxplot([df_e1['anomalies_detected'], df_e3['anomalies_detected']],
            labels=['Baseline', 'Stay Alert'])
plt.ylabel('Anomalias detectadas')
plt.title('Comparativo: Ronda Simples vs Stay Alert')
plt.savefig('comparativo.pdf')
```

**Entregável S6:** Tabelas e gráficos prontos para o artigo.

---

## Sprint S7 — Escrita do artigo (Semana 11-14)

### S7.1 — Estrutura sugerida IEEE Access

```
1. Introduction
   - Problema: inspeção de subestações com robôs autônomos
   - Lacuna: navegação reativa inteligente (além de ronda simples)
   - Contribuição: Bellman atratora + Stay Alert

2. Related Work
   - Inspeção robótica de subestações
   - Navegação reativa (Q-learning, campos potenciais)
   - Nav2 e MPPI em aplicações industriais

3. Proposed Method
   - Arquitetura do sistema
   - Equação de Bellman atratora (com prova de convergência)
   - Módulo Stay Alert
   - Integração com Nav2/MPPI

4. Experimental Setup
   - Modelo de subestação no Gazebo Harmonic
   - ROS2 Humble + Nav2 MPPI
   - Fontes de anomalia simuladas
   - Métricas avaliadas

5. Results and Discussion
   - Tabelas comparativas E1-E5
   - Análise estatística (teste t, ANOVA)
   - Gráficos de convergência Q
   - Discussão dos hiperparâmetros (η, α, γ)

6. Conclusion
   - Contribuições
   - Limitações
   - Trabalhos futuros (validação físical — GO2 PRO)
```

### S7.2 — Template IEEE Access

```bash
# Baixar template LaTeX IEEE Access
wget https://template-selector.ieee.org/secure/templateSelector/downloadTemplate?templateId=ieee_access
```

---

## Cronograma resumido

| Sprint | Atividade | Semanas | Entregável |
|---|---|---|---|
| S1 | Ambiente base (ROS2 + Gazebo + Nav2) | 1-2 | Ambiente funcionando |
| S2 | Modelo do robô no Gazebo | 2-3 | Robô simulado navegando |
| S3 | Modelo da subestação | 3-5 | Mundo Gazebo com subestação |
| S4 | Navegação base com Nav2 | 5-6 | Robô nos waypoints de inspeção |
| S5 | Implementação Bellman Atratora | 6-9 | Stay Alert funcionando |
| S6 | Coleta de métricas | 9-11 | Dados para o artigo |
| S7 | Escrita do artigo | 11-14 | Submissão IEEE Access |

**Tempo total estimado:** 14 semanas (~3,5 meses)

---

## Decisões de projeto

| Decisão | Escolha | Justificativa |
|---|---|---|
| Robô simulado | TurtleBot3 (ou GO2 simplificado) | Foco no algoritmo, não no modelo |
| Planner global | Nav2 NavFn / MPPI | Padrão industrial, publicável |
| Aprendizado | Q-learning tabular (início) | Interpretável, convergência garantida |
| Mundo | Gazebo Harmonic SDF | Compatível com ROS2 Humble |
| Anomalias | Simuladas por proximidade | Independente de hardware real |
| Validação real | GO2 PRO (se houver tempo) | Seção de trabalhos futuros |

---

## Separação do projeto CGW Autopilot

Este workspace é **completamente independente** do CGW Autopilot:

```
~/tese_ws/     ← simulação / tese (este plano)
~/ros2_ws/     ← CGW Autopilot / GO2 PRO físico (não modificar)
```

Nenhum arquivo é compartilhado entre os dois projetos. O único ponto de contato futuro é a validação no GO2 PRO físico (Sprint opcional após S7).

---

## Referências chave

- Bellman, R. (1957). Dynamic Programming
- Sutton & Barto — Reinforcement Learning: An Introduction (2018)
- Macenski et al. — Nav2: The new navigation system for ROS (2023)
- Williams et al. — MPPI: Model Predictive Path Integral Control (2017)
- IEEE Access — Author Guidelines: https://ieeeaccess.ieee.org/
