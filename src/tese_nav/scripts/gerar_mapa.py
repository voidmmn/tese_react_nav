#!/usr/bin/env python3
"""
Gera o mapa de ocupação 2D da subestação a partir da geometria conhecida do
mundo (subestacao.sdf), em vez de mapear com SLAM. Produz um par .pgm/.yaml
no formato do nav2 map_server, com o frame `map` alinhado ao frame do mundo
do Gazebo (logo, waypoints em coordenadas do mundo = goals diretos).

Saída: config/maps/subestacao.pgm + subestacao.yaml

Uso:
    python3 gerar_mapa.py [dir_saida]
"""
import os
import sys

# --------------------------------------------------------------------------- #
# Obstáculos (centro_x, centro_y, tamanho_x, tamanho_y) em metros — coerentes
# com worlds/subestacao.sdf. Cercas já com a rotação aplicada (extensão final).
OBSTACLES = [
    # cercas perimetrais (anel de 50x50)
    (0.0, 25.0, 50.0, 0.2),    # norte
    (0.0, -25.0, 50.0, 0.2),   # sul
    (25.0, 0.0, 0.2, 50.0),    # leste (rotacionada)
    (-25.0, 0.0, 0.2, 50.0),   # oeste (rotacionada)
    # equipamentos
    (10.0, 10.0, 3.0, 2.0),    # transformador_1
    (-5.0, 5.0, 1.0, 1.0),     # disjuntor_1
    (0.0, 15.0, 8.0, 0.3),     # barramento_entrada
]

RESOLUTION = 0.05          # m/pixel
MARGIN = 1.0               # m de borda além das cercas
MIN_XY, MAX_XY = -25.0, 25.0

# valores PGM (convenção nav2): 0=ocupado(preto), 254=livre, 205=desconhecido
FREE, OCC = 254, 0


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else \
        os.path.join(os.path.dirname(__file__), '..', 'config', 'maps')
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    origin_x = MIN_XY - MARGIN
    origin_y = MIN_XY - MARGIN
    span = (MAX_XY - MIN_XY) + 2 * MARGIN          # 52 m
    n = int(round(span / RESOLUTION))               # nº de células por lado

    # grade inicial toda livre (linha 0 = topo = maior y)
    grid = bytearray([FREE]) * (n * n)

    def stamp(cx, cy, sx, sy):
        x0, x1 = cx - sx / 2.0, cx + sx / 2.0
        y0, y1 = cy - sy / 2.0, cy + sy / 2.0
        col0 = max(0, int((x0 - origin_x) / RESOLUTION))
        col1 = min(n - 1, int((x1 - origin_x) / RESOLUTION))
        row0 = max(0, int((y0 - origin_y) / RESOLUTION))
        row1 = min(n - 1, int((y1 - origin_y) / RESOLUTION))
        for r in range(row0, row1 + 1):
            img_row = (n - 1) - r          # flip vertical (PGM: topo primeiro)
            base = img_row * n
            for c in range(col0, col1 + 1):
                grid[base + c] = OCC

    for (cx, cy, sx, sy) in OBSTACLES:
        stamp(cx, cy, sx, sy)

    pgm_path = os.path.join(out_dir, 'subestacao.pgm')
    yaml_path = os.path.join(out_dir, 'subestacao.yaml')

    with open(pgm_path, 'wb') as f:
        f.write(f'P5\n{n} {n}\n255\n'.encode())
        f.write(bytes(grid))

    with open(yaml_path, 'w') as f:
        f.write(f"""image: subestacao.pgm
mode: trinary
resolution: {RESOLUTION}
origin: [{origin_x}, {origin_y}, 0.0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.25
""")

    occ = sum(1 for b in grid if b == OCC)
    print(f'Mapa {n}x{n} ({span:.0f}x{span:.0f} m @ {RESOLUTION} m/px), '
          f'{occ} células ocupadas')
    print(f'  {pgm_path}')
    print(f'  {yaml_path}')


if __name__ == '__main__':
    main()
