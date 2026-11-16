#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figura da arquitetura de duas camadas (Capitulo 4), em PDF vetorial.
=====================================================================

POR QUE SCRIPT, E NAO IMAGEM GERADA. A versao anterior era PNG de 1200x1200 px
posto em \\textwidth (455 pt = 6,32 pol), isto e, 190 dpi -- a figura de menor
resolucao do documento. Vetor nao tem resolucao: e nitida em qualquer largura.
Alem disso a versao anterior rotulava a camada deliberativa como "Sensoriamento
ativo", que nao descreve o que ela faz, repetia a maquina de estados que ja tem
figura propria (fig. 13) e trazia miniaturas ilustrativas do planejador e do
MPPI que nao mostravam nada -- tanto que a legenda precisava declarar-se
"ilustrativa".

O QUE ESTA FIGURA AFIRMA, e de onde vem cada afirmacao:

  - Topologia e nomes dos nos e topicos: lidos de src/tese_nav/tese_nav/
    (stay_alert_node.py, mission_node.py, bellman_node.py, anomaly_simulator.py).
  - Taxas de cada componente: Tabela 4.3 da tese (tab:prop-taxas).
  - O Nav2 como UNICO produtor de /cmd_vel: por isso UMA so seta sai para o
    ambiente, e ela sai do Nav2. E a afirmacao central da Secao 4.1.
  - mission_node e stay_alert_node disputam a MESMA interface NavigateToPose:
    as duas setas convergem no mesmo ponto de entrada do Nav2. E a arbitragem.
  - A tabela Q aparece destacada e em cinza porque e passiva: atualizada e
    publicada, nao atua sobre o comportamento avaliado.
  - O relogio do decaimento aparece marcado como DE PAREDE, que e a unica
    excecao da Tabela 4.3 e o defeito declarado na Secao 6.13.
  - A serie de Phi nao e desenhada a mao: e CALCULADA com a mesma semantica do
    AttractionField (acumulo por evento, decaimento multiplicativo por periodo),
    de sorte que os cruzamentos de limiar na figura saem da conta e nao do lapis.

Uso: python3 gerar_fig_arquitetura.py [diretorio_de_saida]
     (padrao: ~/tese_ws/docs/tese/figuras)
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 9,
    'mathtext.fontset': 'cm',
    'pdf.fonttype': 42,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.02,
})

AZUL = '#1f4e79'
AZUL_C = '#dce9f5'
LARANJA = '#c1440e'
LARANJA_C = '#fdeae0'
VERDE = '#2e7d32'
CINZA = '#8a8a8a'
CINZA_C = '#ededed'
PRETO = '#222222'


# ---------------------------------------------------------------- utilitarios
def caixa(ax, x0, y0, x1, y1, cor_borda, cor_fundo, lw=1.1, r=0.9, z=2, ls='-'):
    p = FancyBboxPatch((x0, y0), x1 - x0, y1 - y0,
                       boxstyle='round,pad=0,rounding_size=%.2f' % r,
                       linewidth=lw, edgecolor=cor_borda, facecolor=cor_fundo,
                       linestyle=ls, zorder=z)
    ax.add_patch(p)
    return p


def texto(ax, x, y, s, cor=PRETO, tam=8.0, peso='normal', ha='center',
          va='center', z=5, it=False):
    ax.text(x, y, s, color=cor, fontsize=tam, fontweight=peso, ha=ha, va=va,
            zorder=z, style='italic' if it else 'normal')


def seta(ax, pontos, cor, lw=1.3, ls='-', z=4, cabeca=7.0):
    """Polilinha ortogonal com cabeca de seta no ultimo segmento."""
    xs = [p[0] for p in pontos]
    ys = [p[1] for p in pontos]
    ax.plot(xs[:-1] + [xs[-1]], ys[:-1] + [ys[-1]], color=cor, lw=lw,
            ls=ls, zorder=z, solid_capstyle='round')
    ax.annotate('', xy=pontos[-1], xytext=pontos[-2],
                arrowprops=dict(arrowstyle='-|>', color=cor, lw=lw,
                                mutation_scale=cabeca, shrinkA=0, shrinkB=0),
                zorder=z + 1)


# ------------------------------------------------- a serie de Phi, calculada
def serie_phi(n=420, periodo=14, lam=0.78, limiar=0.55):
    """Acumulo por evento e decaimento multiplicativo por periodo.

    Mesma semantica do AttractionField: o evento soma ao acumulador; uma vez
    por periodo o acumulador e multiplicado por lambda. O decaimento sai em
    degraus justamente por ser aplicado uma vez por periodo, e nao a cada
    amostra -- que e o que a figura precisa mostrar.
    """
    eventos = {40: 0.52, 55: 0.46, 150: 0.30, 232: 0.78, 246: 0.34, 330: 0.26}
    phi = np.zeros(n)
    acc = 0.0
    for t in range(n):
        acc += eventos.get(t, 0.0)
        if t > 0 and t % periodo == 0:
            acc *= lam
        phi[t] = acc
    return phi, limiar


# ------------------------------------------------------------------- a figura
def desenhar(destino):
    fig, ax = plt.subplots(figsize=(7.8, 5.9))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # ---------------------------------------------------------- faixas-camada
    caixa(ax, 21.5, 57, 76.5, 97.5, AZUL, AZUL_C, lw=1.0, r=1.4, z=1)
    texto(ax, 23.5, 95.0, 'CAMADA DELIBERATIVA', AZUL, 8.2, 'bold', ha='left')
    caixa(ax, 21.5, 4.0, 76.5, 41.0, LARANJA, LARANJA_C, lw=1.0, r=1.4, z=1)
    texto(ax, 23.5, 38.4, 'CAMADA REATIVA — Stay Alert', LARANJA, 8.2, 'bold',
          ha='left')

    # ------------------------------------------------------- fonte de eventos
    caixa(ax, 0.5, 13, 19.5, 79, CINZA, '#ffffff', lw=1.0, r=1.0, z=2)
    texto(ax, 10, 75.3, 'Eventos (oráculo)', PRETO, 7.6, 'bold')
    texto(ax, 10, 71.8, r'$2$ Hz · relógio simulado', CINZA, 6.3)
    for rot, yy in (('térmica', 64.5), ('acústica', 60), ('risco', 55.5)):
        ax.plot([3.2, 4.8], [yy, yy], color=LARANJA, lw=1.4, zorder=3)
        texto(ax, 5.6, yy, rot, PRETO, 6.9, ha='left')
    texto(ax, 10, 48.5, 'modalidade e', CINZA, 6.3)
    texto(ax, 10, 45.4, 'intensidade; posição', CINZA, 6.3)
    texto(ax, 10, 42.3, 'e identidade do alvo', CINZA, 6.3)
    texto(ax, 10, 35.5, 'detecção e', CINZA, 6.3, it=True)
    texto(ax, 10, 32.4, 'classificação são', CINZA, 6.3, it=True)
    texto(ax, 10, 29.3, 'abstraídas: não são', CINZA, 6.3, it=True)
    texto(ax, 10, 26.2, 'contribuição da tese', CINZA, 6.3, it=True)
    texto(ax, 10, 17.2, r'$\mathtt{anomaly\_simulator}$', CINZA, 6.1)

    # ------------------------------------------------- deliberativa: conteudo
    texto(ax, 32.5, 88.0, 'duas fontes, uma só interface', PRETO, 6.1)
    caixa(ax, 24, 69.5, 41, 84.5, AZUL, '#ffffff', z=3)
    texto(ax, 32.5, 81.2, r'$\mathtt{mission\_node}$', AZUL, 7.0, 'bold')
    texto(ax, 32.5, 76.8, 'ronda por', PRETO, 7.2)
    texto(ax, 32.5, 73.4, 'waypoints', PRETO, 7.2, it=True)

    caixa(ax, 45.5, 59.5, 75, 91.5, AZUL, '#ffffff', z=3)
    texto(ax, 47, 88.8, 'Nav2', AZUL, 7.8, 'bold', ha='left')
    caixa(ax, 47.5, 72.5, 60, 83.5, AZUL, AZUL_C, lw=0.9, r=0.6, z=4)
    texto(ax, 53.7, 79.5, 'NavfnPlanner', PRETO, 6.9)
    texto(ax, 53.7, 75.8, 'rota global', CINZA, 6.3)
    caixa(ax, 62, 72.5, 73.5, 83.5, AZUL, AZUL_C, lw=0.9, r=0.6, z=4)
    texto(ax, 67.7, 79.5, 'MPPI', PRETO, 7.2, 'bold')
    texto(ax, 67.7, 75.8, r'$20$ Hz', CINZA, 6.3)
    seta(ax, [(60, 78), (62, 78)], AZUL, lw=1.1, z=5, cabeca=6)

    caixa(ax, 47.5, 62, 73.5, 70, AZUL, '#f7fbff', lw=0.9, r=0.6, z=4)
    texto(ax, 60.5, 67.3, 'costmap', PRETO, 6.9, it=True)
    texto(ax, 60.5, 64.1, r'global $1$ Hz · local $5$ Hz', CINZA, 6.3)
    seta(ax, [(67.7, 70), (67.7, 72.5)], AZUL, lw=1.0, ls=(0, (2.5, 1.6)), z=5,
         cabeca=6)

    # ------------------------------------------------------ reativa: conteudo
    caixa(ax, 24, 12.5, 49, 33, LARANJA, '#ffffff', z=3)
    texto(ax, 36.5, 30.4, r'Campo $\Phi$ — atração e repulsão', PRETO, 7.0,
          'bold')
    texto(ax, 36.5, 27.4, r'leitura e publicação a $1$ Hz', CINZA, 6.2)

    phi, limiar = serie_phi()
    x0, x1b, y0, y1b = 27.5, 46, 18.5, 25.3
    t = np.linspace(x0, x1b, len(phi))
    esc = (y1b - y0) / max(phi.max(), limiar * 1.6)
    ax.plot([x0, x1b], [y0 + limiar * esc] * 2, color=CINZA, lw=0.9,
            ls=(0, (3, 2)), zorder=5)
    ax.plot(t, y0 + phi * esc, color=LARANJA, lw=1.2, zorder=6)
    texto(ax, x1b - 0.3, y0 + limiar * esc + 1.1, 'limiar', CINZA, 5.9, ha='right')
    ax.plot([x0, x0], [y0, y1b], color=CINZA, lw=0.7, zorder=4)
    ax.plot([x0, x1b], [y0, y0], color=CINZA, lw=0.7, zorder=4)
    texto(ax, x0 - 0.8, y1b, r'$\Phi$', PRETO, 6.8, ha='right')
    texto(ax, (x0 + x1b) / 2, y0 - 1.7, 'tempo', CINZA, 5.9)

    ax.plot([25.6], [14.7], marker='o', ms=2.8, color=VERDE, zorder=6)
    texto(ax, 26.5, 14.7, 'decaimento: relógio DE PAREDE', VERDE, 6.1, ha='left')

    caixa(ax, 24, 5.5, 49, 11.3, CINZA, CINZA_C, lw=0.9, r=0.6, ls=(0, (3, 2)),
          z=3)
    texto(ax, 36.5, 9.4, r'tabela $Q(s,a)$ com termo $\eta\Phi$', CINZA, 6.6)
    texto(ax, 36.5, 7.0, 'passiva: não atua no comportamento', CINZA, 6.1,
          it=True)
    seta(ax, [(36.5, 12.5), (36.5, 11.3)], CINZA, lw=0.9, ls=(0, (2.5, 1.6)),
         z=5, cabeca=6)

    caixa(ax, 52.5, 12.5, 75, 33, LARANJA, '#ffffff', z=3)
    texto(ax, 63.7, 30.4, 'Supervisor Stay Alert', PRETO, 7.2, 'bold')
    texto(ax, 63.7, 27.4, r'$5$ Hz · guardas em ordem', CINZA, 6.2)
    caixa(ax, 53.3, 21.2, 74.2, 25.2, LARANJA, LARANJA_C, lw=0.9, r=0.5, z=4)
    texto(ax, 63.7, 23.2, 'precedência CATEGÓRICA', LARANJA, 6.3, 'bold')
    texto(ax, 63.7, 18.3, 'risco acima do limiar domina', PRETO, 6.3)
    texto(ax, 63.7, 15.8, 'qualquer atração, sem soma', PRETO, 6.3)
    seta(ax, [(49, 23.2), (52.5, 23.2)], LARANJA, lw=1.2, z=5, cabeca=6.5)
    seta(ax, [(19.5, 23.2), (24, 23.2)], LARANJA, lw=1.2, z=5, cabeca=6.5)

    # ---------------------------------------------------------- o ambiente
    caixa(ax, 85, 22, 99.5, 84, CINZA, '#ffffff', lw=1.0, r=1.0, z=2)
    texto(ax, 92.2, 80.3, 'Gazebo Fortress', PRETO, 7.4, 'bold')
    texto(ax, 92.2, 76.9, 'mundo e robô', CINZA, 6.5)
    ax.add_patch(Circle((92.2, 55), 4.0, facecolor='#f2f2f2', edgecolor=CINZA,
                        lw=1.0, zorder=3))
    ax.add_patch(Circle((92.2, 55), 1.3, facecolor=CINZA, edgecolor='none',
                        zorder=4))
    for ang in range(0, 360, 30):
        a = np.deg2rad(ang)
        ax.plot([92.2 + 4.4 * np.cos(a), 92.2 + 7.2 * np.cos(a)],
                [55 + 4.4 * np.sin(a), 55 + 7.2 * np.sin(a)],
                color='#c9d9e8', lw=0.8, zorder=2)
    texto(ax, 92.2, 41.5, 'LiDAR e odometria', CINZA, 6.3)
    texto(ax, 92.2, 33.5, r'$\mathtt{map}\!\to\!\mathtt{odom}$ fixa:', CINZA, 6.1)
    texto(ax, 92.2, 30.4, 'deriva de localização', CINZA, 6.1)
    texto(ax, 92.2, 27.3, 'não é modelada', CINZA, 6.1)

    # ------------------------------------------------- setas entre as camadas
    seta(ax, [(57, 33), (57, 44.0), (30, 44.0), (30, 69.5)], LARANJA)
    texto(ax, 43, 45.5, r'$\mathtt{/stay\_alert/active}$ — pausa e retoma a ronda',
          LARANJA, 6.4)

    seta(ax, [(65, 33), (65, 50.5), (43.5, 50.5), (43.5, 78), (45.5, 78)],
         LARANJA)
    texto(ax, 54, 54.2, 'preempção: meta de aproximação ou de recuo', LARANJA, 6.4)
    texto(ax, 54, 51.8, r'$\mathtt{NavigateToPose}$ — a mesma interface', LARANJA,
          6.4)
    seta(ax, [(41, 78), (45.5, 78)], AZUL, lw=1.2, cabeca=6.5)
    ax.plot([45.5], [78], marker='o', ms=4.0, color=PRETO, zorder=7)

    seta(ax, [(71, 33), (71, 62)], VERDE)
    texto(ax, 72.1, 48.5, 'zona de exclusão:', VERDE, 6.3, ha='left')
    texto(ax, 72.1, 46.1, 'a repulsão projetada', VERDE, 6.3, ha='left')
    texto(ax, 72.1, 43.7, 'no costmap', VERDE, 6.3, ha='left', it=True)

    # ----------------------------------------------------- ambiente: ida/volta
    seta(ax, [(75, 74), (85, 74)], AZUL, lw=1.7, cabeca=8.5)
    texto(ax, 80, 77.6, r'$\mathtt{/cmd\_vel}$', AZUL, 6.8, 'bold')
    texto(ax, 79.8, 70.6, 'o Nav2 é o', AZUL, 5.9)
    texto(ax, 79.8, 68.4, 'único produtor', AZUL, 5.9)

    seta(ax, [(92.2, 22), (92.2, 1.6), (10, 1.6), (10, 13)], CINZA, lw=1.2)
    texto(ax, 51, 2.8, 'leituras e pose do robô', CINZA, 6.2)

    fig.savefig(destino)
    plt.close(fig)
    print('gravado: %s' % destino)


if __name__ == '__main__':
    saida = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
        '~/tese_ws/docs/tese/figuras')
    desenhar(os.path.join(saida, 'fig_arquitetura.pdf'))
