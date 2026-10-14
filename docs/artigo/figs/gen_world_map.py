#!/usr/bin/env python3
"""Gera o mapa esquemático do mundo (Fig. world) a partir das coordenadas
reais do cenário (subestacao.sdf / anomaly_simulator / waypoints.yaml).
Saída: world_map.pdf (vetorial p/ LaTeX) e world_map.png (preview).
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

R = 5.0  # raio de detecção

# equipamentos: (nome, x, y, largura, altura)
equip = [
    ('Transformer', 10, 10, 3, 2),
    ('Breaker',      -5, 5, 1, 1),
    ('Busbar',        0, 15, 8, 0.3),
]
# waypoints na ordem da ronda (spawn = retorno = (-10,-10))
wps = [(-10, -10), (13, -8), (13, 10), (0, 11), (-8, 5), (-10, -10)]
# eventos de atração (default): (x, y, tipo)
anomalies = [(10, 10, 'thermal'), (0, 15, 'thermal'), (-5, 5, 'acoustic')]
hazard = (2, -13)

fig, ax = plt.subplots(figsize=(5.0, 5.0))

# cerca/limite (50x50, centrado na origem)
ax.add_patch(Rectangle((-25, -25), 50, 50, fill=False, ec='0.6',
                        lw=1.2, ls='-'))

# equipamentos
for name, x, y, w, h in equip:
    ax.add_patch(Rectangle((x - w/2, y - h/2), w, h, facecolor='0.8',
                           edgecolor='0.3', lw=1.0, zorder=2))
    ax.text(x, y - 1.4, name, ha='center', va='top', fontsize=7, color='0.3')

# ronda (caminho tracejado + waypoints numerados)
xs, ys = zip(*wps)
ax.plot(xs, ys, '--', color='tab:blue', lw=1.3, zorder=3, label='Patrol route')
for i, (x, y) in enumerate(wps[:-1]):
    ax.plot(x, y, 'o', color='tab:blue', ms=7, zorder=4)
    ax.text(x + 0.6, y + 0.6, f'W{i}', fontsize=8, color='tab:blue', zorder=5)
ax.text(-10, -10 - 1.6, 'start/return', ha='center', va='top', fontsize=7,
        color='tab:blue')

# anomalias (atração) com raio de detecção
for x, y, t in anomalies:
    ax.add_patch(Circle((x, y), R, fill=False, ec='tab:red', ls=':', lw=1.0,
                        alpha=0.7, zorder=1))
    m = '^' if t == 'thermal' else 's'
    ax.plot(x, y, m, color='tab:red', ms=9, zorder=5)

# perigo (repulsão) com raio de detecção
hx, hy = hazard
ax.add_patch(Circle((hx, hy), R, fill=False, ec='tab:orange', ls=':', lw=1.0,
                    alpha=0.8, zorder=1))
ax.plot(hx, hy, 'X', color='tab:orange', ms=11, zorder=5)
ax.text(hx + 0.7, hy, 'hazard', fontsize=7, color='tab:orange', va='center')

# legenda manual (proxies)
from matplotlib.lines import Line2D
legend = [
    Line2D([0], [0], marker='o', color='tab:blue', ls='--', label='patrol / waypoint'),
    Line2D([0], [0], marker='^', color='tab:red', ls='', label='thermal anomaly'),
    Line2D([0], [0], marker='s', color='tab:red', ls='', label='acoustic anomaly'),
    Line2D([0], [0], marker='X', color='tab:orange', ls='', label='hazard'),
    Line2D([0], [0], color='tab:red', ls=':', label=f'detection radius (R={R:.0f} m)'),
]
ax.legend(handles=legend, loc='lower right', fontsize=6.5, framealpha=0.9)

ax.set_xlim(-16, 20); ax.set_ylim(-18, 20)
ax.set_aspect('equal')
ax.set_xlabel('x [m]'); ax.set_ylabel('y [m]')
ax.grid(True, ls=':', alpha=0.3)
fig.tight_layout()
fig.savefig('world_map.pdf'); fig.savefig('world_map.png', dpi=150)
print('salvo: world_map.pdf / world_map.png')
