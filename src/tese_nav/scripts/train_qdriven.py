#!/usr/bin/env python3
"""
Treino do baseline Q-DRIVEN num sim cinemático rápido (Python puro).
====================================================================

Aprende Q(s,a) para a subtarefa reativa (aproximar de anomalia / afastar de
perigo) com recompensa AUMENTADA pelo sinal afetivo Φ (reward augmentation).
Milhares de episódios em segundos; a política greedy resultante é salva em
config/qtable_qdriven.json e carregada pelo qdriven_node no Gazebo.

Uso: python3 train_qdriven.py [n_episodes]
"""
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tese_nav', 'utils'))
from qdriven_core import ACTIONS, ACTION_CMD, discretize, bearing_to, wrap  # noqa

OUT = os.path.join(HERE, '..', 'config', 'qtable_qdriven.json')

# hiperparâmetros
ALPHA, GAMMA = 0.2, 0.95
EPS0, EPS_MIN = 1.0, 0.05
ETA = 0.5                 # peso do Φ na recompensa (reward augmentation)
DT = 0.2
MAX_STEPS = 120
STANDOFF = 1.8            # anomalia inspecionada
SAFE = 6.0               # perigo evitado
COLLISION = 0.5
K_PROG = 3.0
STEP_PEN = -0.05
R_GOAL, R_CRASH = 20.0, -20.0
DET_R = 5.0


def q_get(Q, s):
    return Q.setdefault(s, [0.0] * len(ACTIONS))


def run(n_episodes):
    Q = {}
    rng = random.Random(0)
    for ep in range(n_episodes):
        eps = max(EPS_MIN, EPS0 * (1.0 - ep / (0.9 * n_episodes)))
        ev_type = 'anomaly' if rng.random() < 0.5 else 'hazard'
        intensity = rng.uniform(0.7, 0.95)
        # evento em pos. aleatória dentro do alcance; robô na origem, yaw aleatório
        d0 = rng.uniform(1.5, DET_R)
        ang = rng.uniform(-math.pi, math.pi)
        ex, ey = d0 * math.cos(ang), d0 * math.sin(ang)
        rx = ry = 0.0
        ryaw = rng.uniform(-math.pi, math.pi)
        prev_d = math.hypot(ex - rx, ey - ry)

        for _ in range(MAX_STEPS):
            bearing = wrap(bearing_to(rx, ry, ryaw, ex, ey))
            s = discretize(ev_type, prev_d, bearing)
            qs = q_get(Q, s)
            if rng.random() < eps:
                a = rng.randrange(len(ACTIONS))
            else:
                a = max(range(len(ACTIONS)), key=lambda i: qs[i])

            lin, angv = ACTION_CMD[ACTIONS[a]]
            ryaw = wrap(ryaw + angv * DT)
            rx += lin * math.cos(ryaw) * DT
            ry += lin * math.sin(ryaw) * DT
            d = math.hypot(ex - rx, ey - ry)

            phi = intensity / max(d, 0.5)      # magnitude do campo
            done = False
            if ev_type == 'anomaly':
                r = K_PROG * (prev_d - d) + ETA * phi + STEP_PEN
                if d <= STANDOFF:
                    r += R_GOAL; done = True
            else:  # hazard: recompensa por AFASTAR; Φ entra como penalidade
                r = K_PROG * (d - prev_d) - ETA * phi + STEP_PEN
                if d < COLLISION:
                    r += R_CRASH; done = True
                elif d >= SAFE:
                    r += R_GOAL; done = True

            bearing2 = wrap(bearing_to(rx, ry, ryaw, ex, ey))
            s2 = discretize(ev_type, d, bearing2)
            q2 = q_get(Q, s2)
            target = r + (0.0 if done else GAMMA * max(q2))
            qs[a] += ALPHA * (target - qs[a])
            prev_d = d
            if done:
                break

    # serializa: "tb,db,bb" -> [q...]
    out = {','.join(map(str, k)): v for k, v in Q.items()}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as fh:
        json.dump({'meta': {'episodes': n_episodes, 'eta': ETA,
                            'actions': list(ACTIONS)}, 'q': out}, fh, indent=1)
    print(f'treino: {n_episodes} episódios, |Q|={len(Q)} estados -> {OUT}')
    return Q


def evaluate(Q, trials=2000):
    """Sanidade: taxa de sucesso greedy (anomalia alcançada / perigo evitado)."""
    rng = random.Random(1)
    ok = 0
    for _ in range(trials):
        ev_type = 'anomaly' if rng.random() < 0.5 else 'hazard'
        d0 = rng.uniform(1.5, DET_R); ang = rng.uniform(-math.pi, math.pi)
        ex, ey = d0 * math.cos(ang), d0 * math.sin(ang)
        rx = ry = 0.0; ryaw = rng.uniform(-math.pi, math.pi)
        prev_d = d0
        for _ in range(MAX_STEPS):
            bearing = wrap(bearing_to(rx, ry, ryaw, ex, ey))
            qs = Q.get(discretize(ev_type, prev_d, bearing), [0.0] * 4)
            a = max(range(len(ACTIONS)), key=lambda i: qs[i])
            lin, angv = ACTION_CMD[ACTIONS[a]]
            ryaw = wrap(ryaw + angv * DT)
            rx += lin * math.cos(ryaw) * DT; ry += lin * math.sin(ryaw) * DT
            d = math.hypot(ex - rx, ey - ry)
            if ev_type == 'anomaly' and d <= STANDOFF:
                ok += 1; break
            if ev_type == 'hazard' and d >= SAFE:
                ok += 1; break
            if ev_type == 'hazard' and d < COLLISION:
                break
            prev_d = d
    print(f'sanidade greedy: {ok}/{trials} = {100*ok/trials:.1f}% sucesso')


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 40000
    Q = run(n)
    evaluate(Q)
