#!/usr/bin/env bash
# Disparo NOTURNO único da bateria E1–E5 (agendado via cron às 19h).
# - auto-remove a entrada do cron (roda só uma vez)
# - limpeza de segurança (mata restos de sim) -> evita o vazamento de órfãos
# - roda os 50 experimentos (rodar_experimentos.sh 10 600)
# - roda a análise (resumo + boxplots)
# Log: results/noturna.log (via redirecionamento do cron).
# Nota: sem 'set -u' (setup.bash do ROS usa variáveis não definidas).
set -o pipefail
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH
WS="$HOME/tese_ws"
cd "$WS" || exit 1

echo "===== BATERIA NOTURNA: início $(date '+%F %T') ====="

# 1) remove a própria entrada do cron (one-shot)
( crontab -l 2>/dev/null | grep -v 'run_bateria_noturna.sh' ) | crontab - 2>/dev/null
echo "cron: entrada removida (execução única)"

# 2) limpeza de segurança (o cmdline deste wrapper NÃO contém os padrões,
#    então pkill -f não se auto-mata como num shell interativo)
pkill -9 -f "fake_scan_publisher|robot_state_publisher|parameter_bridge|static_transform_publisher|ros_gz_sim|bellman_node|stay_alert_node|mission_node|metrics_node|anomaly_simulator|component_container|experimento.launch|rodar_experimentos|ign gazebo" 2>/dev/null
pkill -9 -x ruby 2>/dev/null
rm -f /dev/shm/fastrtps_* /dev/shm/sem.fastrtps_* 2>/dev/null
sleep 5

# 3) garante results/ limpo (arquiva qualquer CSV/log avulso)
mkdir -p "$WS/results/_pre_noturna"
mv "$WS"/results/metrics_*.csv "$WS"/results/launch_*.log "$WS"/results/bateria.log \
   "$WS/results/_pre_noturna/" 2>/dev/null

# 4) bateria principal (10 reps × 9 configs = 90 runs): E1, E0(η=0), E2/E3/E4
#    (sweep η), E5(adverso), APF, RHM/RHB (perigo-na-rota método/baseline)
echo ">>> rodando matriz principal 10x9 ($(date '+%T'))..."
bash "$WS/src/tese_nav/scripts/rodar_experimentos.sh" 10 600
echo ">>> matriz principal concluída $(date '+%F %T')"

# 4b) sweep de robustez a ruído de percepção (R1#3): E3 método (η=0.5, default)
#     com ruído gaussiano moderado e alto na posição/intensidade do evento
echo ">>> sweep de ruído ($(date '+%T'))..."
NOISE_POS=0.3 NOISE_INT=0.05 EXPERIMENTS="N1 0.5 true default stay_alert" \
  bash "$WS/src/tese_nav/scripts/rodar_experimentos.sh" 10 600
NOISE_POS=0.6 NOISE_INT=0.10 EXPERIMENTS="N2 0.5 true default stay_alert" \
  bash "$WS/src/tese_nav/scripts/rodar_experimentos.sh" 10 600
echo ">>> sweep de ruído concluído $(date '+%F %T')"

# 5) análise (resumo_experimentos.csv + box_*.pdf)
echo ">>> análise..."
python3 "$WS/src/tese_nav/scripts/analise_resultados.py" "$WS/results" || \
  echo "[aviso] análise falhou — CSVs estão salvos, rodar manualmente depois"

echo "===== BATERIA NOTURNA: fim $(date '+%F %T') ====="
