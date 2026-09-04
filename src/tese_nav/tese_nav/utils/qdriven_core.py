"""
Núcleo compartilhado do baseline Q-DRIVEN (reward-augmented Q-learning).
=======================================================================

Discretização de estado, ações e recompensa — IDÊNTICOS entre o treino
(train_qdriven.py, sim cinemático rápido) e a execução (qdriven_node.py no
Gazebo), para que a Q-table transfira. É o baseline "RL comportamental": Q(s,a)
seleciona a ação executada (ε-greedy), com o sinal afetivo Φ somado à recompensa
(reward augmentation), contrastando com nossa camada reativa por limiar.

Estado (relativo ao robô, do evento mais próximo relevante):
    (tipo, bucket_distância, bucket_rumo)
  tipo         : 0 = anomalia (aproximar), 1 = perigo (afastar)
  bucket_dist  : 0..3  (faixas de 1.5 m; 3 = >=4.5 m)
  bucket_rumo  : 0..7  (setor de 45° do rumo relativo)

Ações: forward, left, right, stop.
"""
import math

ACTIONS = ('forward', 'left', 'right', 'stop')

# (linear m/s, angular rad/s) por ação
ACTION_CMD = {
    'forward': (0.30, 0.0),
    'left':    (0.12, 0.7),
    'right':   (0.12, -0.7),
    'stop':    (0.0, 0.0),
}

N_DIST = 4
N_BEAR = 8


def discretize(ev_type, dist, bearing):
    """ev_type: 'anomaly'|'hazard'; dist (m); bearing (rad, relativo ao robô)."""
    tb = 0 if ev_type == 'anomaly' else 1
    db = min(int(dist / 1.5), N_DIST - 1)
    b = (bearing + math.pi) % (2 * math.pi)
    bb = min(int(b / (2 * math.pi / N_BEAR)), N_BEAR - 1)
    return (tb, db, bb)


def bearing_to(rx, ry, ryaw, ex, ey):
    """Rumo relativo (rad) do evento (ex,ey) visto do robô em (rx,ry,ryaw)."""
    return math.atan2(ey - ry, ex - rx) - ryaw


def wrap(a):
    return math.atan2(math.sin(a), math.cos(a))
