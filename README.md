# tese_ws — Simulação da Tese de Doutorado

Workspace ROS 2 da simulação para a tese **"Navegação Robótica Reativa
Inteligente para Inspeção de Subestações"** — navegação reativa guiada por uma
**equação de Bellman atratora** (modo *Stay Alert*): um termo de
atração/repulsão Φ(s,a), derivado de eventos sensoriais, modula a função de
valor em tempo real, fazendo o robô **aproximar-se** de anomalias (Φ>0) e
**afastar-se** de perigos (Φ<0).

**Autor:** Milton Miranda Neto · **Orientador:** Prof. Alexandre Cardoso (UFU)

## Stack

ROS 2 Humble · Gazebo **Fortress** (ign-gazebo 6) · Nav2 (controlador MPPI) ·
AMCL sobre mapa estático · robô diferencial `inspector_bot`.

## Estrutura

```
src/tese_nav/        pacote principal (ver src/tese_nav/README.md)
  tese_nav/          nós: bellman, stay_alert, anomaly_simulator, mission, metrics
  config/            nav2_params, slam_toolbox, bellman_params, waypoints, maps/
  launch/            robot_sim, nav2_amcl, simulation, stay_alert, experimento
  urdf/ worlds/      robô e mundo da subestação
  scripts/           gerar_mapa.py, analise_resultados.py
s1_install.sh        instalação do ambiente (S1, roda com sudo)
s1_postinstall.sh    pós-instalação (rosdep/.bashrc/colcon)
PLANO_SIMULACAO_TESE.md   plano de implementação completo
```

## Uso rápido

```bash
# build
cd ~/tese_ws && colcon build --packages-select tese_nav && source install/setup.bash

# experimento completo (robô + Nav2 + Stay Alert) com visualização
ros2 launch tese_nav experimento.launch.py run_label:=E3 eta:=0.5 rviz:=true
```

Detalhes de execução, experimentos (E1–E5) e análise: `src/tese_nav/README.md`.
