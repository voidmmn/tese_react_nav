#!/usr/bin/env python3
"""Sobrepõe as trajetórias E1 (baseline) e E3 (Stay Alert) ao mapa do cenário.
Lê traj_E1.csv e traj_E3.csv (t,x,y). Saída: traj_overlay.pdf/.png."""
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.lines import Line2D

R = 5.0
equip = [('Transformer', 10, 10, 3, 2), ('Breaker', -5, 5, 1, 1),
         ('Busbar', 0, 15, 8, 0.3)]
anomalies = [(10, 10, 'thermal'), (0, 15, 'thermal'), (-5, 5, 'acoustic')]
hazard = (2, -13)


def load(path):
    xs, ys = [], []
    try:
        with open(path) as f:
            for row in csv.DictReader(f):
                xs.append(float(row['x'])); ys.append(float(row['y']))
    except FileNotFoundError:
        print(f'[aviso] {path} não encontrado')
    return xs, ys


fig, ax = plt.subplots(figsize=(5.2, 5.2))
ax.add_patch(Rectangle((-25, -25), 50, 50, fill=False, ec='0.6', lw=1.2))
for name, x, y, w, h in equip:
    ax.add_patch(Rectangle((x - w/2, y - h/2), w, h, facecolor='0.85',
                           edgecolor='0.4', lw=0.8, zorder=1))
for x, y, t in anomalies:
    ax.add_patch(Circle((x, y), R, fill=False, ec='tab:red', ls=':', lw=0.8,
                        alpha=0.5, zorder=1))
    ax.plot(x, y, '^' if t == 'thermal' else 's', color='tab:red', ms=8, zorder=4)
ax.add_patch(Circle(hazard, R, fill=False, ec='tab:orange', ls=':', lw=0.8,
                    alpha=0.6, zorder=1))
ax.plot(*hazard, 'X', color='tab:orange', ms=10, zorder=4)

# trajetórias
x1, y1 = load('traj_E1.csv')
x3, y3 = load('traj_E3.csv')
if x1:
    ax.plot(x1, y1, '-', color='0.45', lw=1.6, zorder=3, label='E1 baseline')
if x3:
    ax.plot(x3, y3, '-', color='tab:blue', lw=1.6, zorder=3,
            label='E3 Stay Alert')
for xs, ys, c in [(x1, y1, '0.45'), (x3, y3, 'tab:blue')]:
    if xs:
        ax.plot(xs[0], ys[0], 'o', color=c, ms=6, zorder=5)   # início

handles = [
    Line2D([0], [0], color='0.45', lw=1.6, label='E1 (baseline patrol)'),
    Line2D([0], [0], color='tab:blue', lw=1.6, label='E3 (Stay Alert)'),
    Line2D([0], [0], marker='^', color='tab:red', ls='', label='thermal anomaly'),
    Line2D([0], [0], marker='s', color='tab:red', ls='', label='acoustic anomaly'),
    Line2D([0], [0], marker='X', color='tab:orange', ls='', label='hazard'),
]
ax.legend(handles=handles, loc='lower right', fontsize=6.5, framealpha=0.9)
ax.set_xlim(-16, 20); ax.set_ylim(-18, 20); ax.set_aspect('equal')
ax.set_xlabel('x [m]'); ax.set_ylabel('y [m]')
ax.grid(True, ls=':', alpha=0.3)
fig.tight_layout()
fig.savefig('traj_overlay.pdf'); fig.savefig('traj_overlay.png', dpi=150)
print('salvo: traj_overlay.pdf / traj_overlay.png')
