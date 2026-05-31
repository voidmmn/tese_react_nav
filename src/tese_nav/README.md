# tese_nav

Pacote ROS2 (Humble / ament_python) da tese — **Bellman atratora + Stay Alert**
para inspeção de subestações. Implementa os Sprints S5/S6 do
`PLANO_SIMULACAO_TESE.md`. É independente do CGW Autopilot (`~/ros2_ws`).

## Componentes

| Nó | Tópicos | Papel |
|---|---|---|
| `anomaly_simulator` | pub `/anomaly/{thermal,acoustic}` ← `/odom` | Anomalias por proximidade (S5.4) |
| `bellman_node` | pub `/stay_alert/attraction`, `/bellman/{td_error,route_deviations}` | Q-learning + campo atrator Φ (S5.3) |
| `stay_alert_node` | pub `/stay_alert/{active,mode,event}` ← `/stay_alert/attraction` | Máquina PATROL ↔ INVESTIGATE |
| `mission_node` | ação `navigate_to_pose`, pub `/mission/*` | Ronda pelos waypoints (S4) |
| `metrics_node` | grava `results/metrics_<label>_*.csv` | Coleta de métricas (S6) |

Fluxo: `anomaly_simulator → bellman_node → stay_alert_node → mission_node`,
com `metrics_node` observando tudo.

## Build

```bash
cd ~/tese_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-select tese_nav
source install/setup.bash
```

## Executar

```bash
# Robô + mundo no Gazebo Fortress + ponte ros_gz (S2) — headless por padrão
ros2 launch tese_nav robot_sim.launch.py            # headless (ign gazebo -s)
ros2 launch tese_nav robot_sim.launch.py headless:=false   # com GUI

# Só a lógica Stay Alert (sem Gazebo/Nav2) — útil para testar com um bag
ros2 launch tese_nav stay_alert.launch.py run_label:=E3

# Simulação completa (S4: + Nav2) — requer Fortress + Nav2 + robô
ros2 launch tese_nav simulation.launch.py run_label:=E3
```

> Inspecionar via CLI exige as mesmas vars de transporte do launch:
> `export IGN_IP=127.0.0.1 IGN_PARTITION=tese_sim` antes de `ign model --list`,
> `ign topic -l`, etc.

## Experimentos (S6.3)

Varia-se `eta` em `config/bellman_params.yaml`: E1 baseline (η=0, ou
`stay_alert` desabilitado), E2 η=0.3, E3 η=0.5, E4 η=0.8, E5 cenário adverso.
10 repetições cada → CSVs em `~/tese_ws/results/`.

## Análise

```bash
python3 src/tese_nav/scripts/analise_resultados.py ~/tese_ws/results
```

> **Nota de ambiente:** o simulador é **Gazebo Fortress** (`ign gazebo`), não
> Harmonic — o `ros_gz` binário do Humble é compilado para Fortress, e o
> pareamento com Harmonic exigiria compilar o ros_gz do fonte. Rodar neste
> Jetson (aarch64) é viável por ele ser dedicado à simulação, mas é pesado em
> ARM. Para as ~25h de experimentos (50 execuções), monitore RTF e temperatura;
> use headless (`ign gazebo -s`, o padrão do `robot_sim.launch.py`) nos lotes.
