#!/usr/bin/env bash
# ============================================================================
# Bateria da RESUBMISSÃO (IEEE Access, Access-2026-46291) — em BLOCOS.
#
# Separado de `rodar_bateria_blocos.sh` de propósito: aquele script é o registro
# do que produziu os dados da submissão anterior e não deve ser alterado.
#
# Colunas da matriz (as 1-9 são as originais; 10-16 são da resubmissão):
#   label eta sa scen react keepout avoid npos nint  sel trig hthr ent ext cfd
#   sel  = selection_mode  'saliency'(método) | 'nearest'(HEU)      [R2#3]
#   trig = trigger_mode    'phi'(método)      | 'range'(HEU)        [R2#3]
#   hthr = hazard_threshold (elegibilidade = PRECEDÊNCIA), -1 = default 0.30 [R2#6]
#   ent/ext = enter/exit_threshold da FSM (ação × largura de histerese)  [R2#6]
#   cfd  = inspect_confirm_dist, 0 = auto (3.3 m)                    [R2#5]
#
# Uso:
#   bash rodar_bateria_resub.sh regressao   # F2.6: gate de reúso (2 runs, ~15 min)
#   bash rodar_bateria_resub.sh noite1      # F4: KOF + HEU + HEU-sel (~8,8 h)
#   bash rodar_bateria_resub.sh noite2      # F5: limiares + histerese (~6,3 h)
# ============================================================================
set -o pipefail
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH
WS="$HOME/tese_ws"
cd "$WS" || exit 1
FASE=${1:?uso: bash rodar_bateria_resub.sh regressao|noite1|noite2}
REPS=${2:-10}
MAXS=${3:-600}

deep_clean() {
  pkill -9 -f "ign gazebo|ign-gazebo|parameter_bridge|robot_state_publisher|ros_gz_sim|static_transform_publisher|fake_scan_publisher|amcl|map_server|controller_server|planner_server|bt_navigator|behavior_server|smoother_server|velocity_smoother|waypoint_follower|lifecycle_manager|component_container|bellman_node|stay_alert_node|apf_node|qdriven_node|mission_node|metrics_node|anomaly_simulator|ros2 launch tese" 2>/dev/null
  pkill -9 -x ruby 2>/dev/null
  ps -eo pid,comm | grep -iE 'ign|ruby|component|amcl|controller_se|planner_se|bt_navig|behavior|smoother|velocity|waypoint|lifecycle|bellman|stay_alert|apf_node|qdriven|mission_no|metrics|anomaly|robot_state|parameter_br|static_transf|fake_scan|map_server' \
    | grep -v grep | awk '{print $1}' | xargs -r kill -9 2>/dev/null
  rm -f /dev/shm/fastrtps_* /dev/shm/sem.fastrtps_* 2>/dev/null
  sleep 12
}

run_block() {
  local label=$1; shift
  echo "===== BLOCO $label ($(date '+%F %T')) ====="
  deep_clean
  EXPERIMENTS="$label $*" bash "$WS/src/tese_nav/scripts/rodar_experimentos.sh" "$REPS" "$MAXS"
  echo "===== FIM BLOCO $label ($(date '+%F %T')) ====="
}

echo "########## BATERIA RESUB [$FASE]: início $(date '+%F %T') ##########"

case "$FASE" in

  # --------------------------------------------------------------------
  # F2.6 — GATE DE REÚSO. Roda E3 com o código novo e os defaults novos.
  # Se divergir do E3 antigo, o reúso de E3/CONF/E5 está inválido e a
  # bateria do método precisa ser refeita (+225 min). Rodar ANTES da noite 1.
  # Label distinto (E3reg) para não sobrescrever o E3 publicado.
  # --------------------------------------------------------------------
  regressao)
    REPS=2
    run_block E3reg  0.5 true  default      stay_alert false true 0.0 0.0
    ;;

  # --------------------------------------------------------------------
  # F4 — noite 1. KOF (atribuição da segurança) + os dois contrastes de
  # HEU nos TRÊS cenários declarados no plano de análise.
  #   HEU    = supervisor genérico completo (nearest + range)  -> R2#3
  #   HEUsel = contraste de UM FATOR (nearest, mas trigger phi)
  # O método nos três cenários é REÚSO de E3/CONF/E5 (não roda aqui).
  # --------------------------------------------------------------------
  noite1)
    run_block KOF     0.0 false route_hazard stay_alert true  false 0.0 0.0
    run_block HEUd    0.5 true  default      stay_alert false true  0.0 0.0 nearest range
    run_block HEUc    0.5 true  conflict     stay_alert false true  0.0 0.0 nearest range
    run_block HEUa    0.5 true  adverse      stay_alert false true  0.0 0.0 nearest range
    run_block HEUseld 0.5 true  default      stay_alert false true  0.0 0.0 nearest phi
    run_block HEUselc 0.5 true  conflict     stay_alert false true  0.0 0.0 nearest phi
    run_block HEUsela 0.5 true  adverse      stay_alert false true  0.0 0.0 nearest phi
    ;;

  # --------------------------------------------------------------------
  # F5 — noite 2. Sensibilidades.
  #   HAZ*  = limiar de modalidade do perigo = PRECEDÊNCIA (não enter_threshold).
  #           Em `conflict`, onde atração e perigo competem de fato.
  #           0.30 é o default -> HAZ30 é a referência da varredura.
  #   HYS*  = separa POSIÇÃO da faixa de LARGURA da faixa (crítica v2 §4):
  #           ref (0.45,0.25) l=0.20 | estreita (0.45,0.35) l=0.10
  #           | deslocada (0.55,0.35) l=0.20
  # --------------------------------------------------------------------
  noite2)
    run_block HAZ20 0.5 true conflict stay_alert false true 0.0 0.0 saliency phi 0.20
    run_block HAZ30 0.5 true conflict stay_alert false true 0.0 0.0 saliency phi 0.30
    run_block HAZ40 0.5 true conflict stay_alert false true 0.0 0.0 saliency phi 0.40
    run_block HYSnar 0.5 true default stay_alert false true 0.0 0.0 saliency phi -1.0 0.45 0.35
    run_block HYSoff 0.5 true default stay_alert false true 0.0 0.0 saliency phi -1.0 0.55 0.35
    ;;

  *) echo "fase desconhecida: $FASE (use regressao|noite1|noite2)"; exit 1 ;;
esac

deep_clean
echo "########## BATERIA RESUB [$FASE]: fim $(date '+%F %T') ##########"
