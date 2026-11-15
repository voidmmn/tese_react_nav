#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figuras conceituais do Capitulo 2 (fundamentacao), em PDF vetorial.
===================================================================

Gera duas figuras:

  fig_shaping.pdf  -- moldagem de recompensa: a forma potencial de Ng, que
                      preserva a politica otima, contra um termo aditivo
                      variante no tempo, que nao preserva. E a figura da
                      Secao 2.2.4.

  fig_mppi.pdf     -- o controlador MPPI: trajetorias sorteadas a partir do
                      estado corrente, custo calculado para cada uma, e o
                      comando devolvido como media ponderada pelo custo. E a
                      figura da Secao 2.5.6.

POR QUE SCRIPT, E NAO IMAGEM GERADA. As duas figuras foram primeiro geradas
como PNG por ferramenta de ilustracao e NAO puderam ser usadas: na da moldagem
os rotulos matematicos saiam rasterizados com franja de cor e um deles estava
errado (lia-se Phi(s) onde cabia Phi(s')); na do MPPI o rotulo "comando
aplicado" saia ilegivel, as trajetorias convergiam no fim em vez de divergir, e
as de BAIXO custo eram as que passavam mais perto do obstaculo -- o inverso do
que o metodo faz. Aqui a geometria nao e desenhada a mao: o custo de cada
trajetoria e CALCULADO (penalidade de proximidade do obstaculo mais penalidade
de desvio da rota) e a cor sai do custo, de sorte que a figura nao pode
contradizer o texto sem que a conta mude junto.

Uso: python3 gerar_figs_fundamentacao.py [diretorio_de_saida]
     (padrao: ~/tese_ws/docs/tese/figuras)
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 9,
    'mathtext.fontset': 'cm',
    'pdf.fonttype': 42,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.02,
})

AZUL = '#1f4e79'
VERDE = '#2e7d32'
AMBAR = '#b26a00'
CINZA = '#9e9e9e'
LARANJA = '#e8590c'


# --------------------------------------------------------------------------
# Figura 1: moldagem de recompensa
# --------------------------------------------------------------------------
def painel_shaping(ax, titulo, rotulos, texto_ciclo, selo, cor_selo):
    """Desenha a cadeia s -> s' -> s'' e o retorno que fecha o ciclo.

    O retorno vai ABAIXO da cadeia, de proposito: na primeira versao ele arqueava
    por cima e cruzava as setas de transicao, de sorte que a figura parecia
    mostrar um salto de s a s'' em vez de um ciclo fechado -- que e a unica coisa
    que ela precisa mostrar. Os rotulos das transicoes tambem subiram, para nao
    disputarem espaco com o arco de retorno.
    """
    xs = [0.0, 2.3, 4.6]
    nomes = ["$s$", "$s'$", "$s''$"]
    cores = ['#dbe7f5', '#dcefdc', '#e6ddf2']

    ax.text(2.3, 2.30, titulo, ha='center', va='center',
            fontsize=10, fontweight='bold', color='#222222')

    for x, nome, cor in zip(xs, nomes, cores):
        ax.add_patch(Circle((x, 0), 0.52, facecolor=cor,
                            edgecolor='#555555', linewidth=1.0, zorder=3))
        ax.text(x, 0, nome, ha='center', va='center', fontsize=11, zorder=4)

    for i in (0, 1):
        ax.add_patch(FancyArrowPatch((xs[i] + 0.56, 0), (xs[i + 1] - 0.56, 0),
                                     arrowstyle='-|>', mutation_scale=11,
                                     linewidth=1.2, color='#555555', zorder=2))
        ax.text((xs[i] + xs[i + 1]) / 2.0, 0.80, rotulos[i],
                ha='center', va='center', fontsize=9.5)

    ax.add_patch(FancyArrowPatch((xs[2], -0.54), (xs[0], -0.54),
                                 connectionstyle='arc3,rad=-0.42',
                                 arrowstyle='-|>', mutation_scale=11,
                                 linewidth=1.2, color='#555555', zorder=2))
    ax.text(2.3, -2.30, texto_ciclo, ha='center', va='center', fontsize=9.0,
            linespacing=1.35)

    ax.add_patch(FancyBboxPatch((0.08, -3.68), 4.44, 0.82,
                                boxstyle='round,pad=0.05,rounding_size=0.10',
                                facecolor=cor_selo + '1f', edgecolor=cor_selo,
                                linewidth=1.1, zorder=3))
    ax.text(2.3, -3.27, selo, ha='center', va='center', fontsize=8.6,
            fontweight='bold', color=cor_selo, zorder=4, linespacing=1.35)

    ax.set_xlim(-0.80, 5.40)
    ax.set_ylim(-4.05, 2.70)
    ax.set_aspect('equal')
    ax.axis('off')


def fig_shaping(destino):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.1, 3.70))

    painel_shaping(
        ax1, 'Forma potencial (Ng, 1999)',
        [r"$\gamma\Phi(s')-\Phi(s)$", r"$\gamma\Phi(s'')-\Phi(s')$"],
        'ao longo de um ciclo fechado,\nas parcelas se cancelam',
        'política ótima preservada', VERDE)

    painel_shaping(
        ax2, 'Termo aditivo variante no tempo',
        [r"$\eta\,\Phi(s,t)$", r"$\eta\,\Phi(s',t')$"],
        'ao longo de um ciclo fechado,\nas parcelas não se cancelam',
        'sem garantia: exige\ndemonstração caso a caso', AMBAR)

    fig.subplots_adjust(wspace=0.06)
    fig.add_artist(plt.Line2D([0.502, 0.502], [0.07, 0.93],
                              transform=fig.transFigure,
                              color='#cccccc', linewidth=0.9))
    fig.savefig(destino)
    plt.close(fig)
    return destino


# --------------------------------------------------------------------------
# Figura 2: MPPI
# --------------------------------------------------------------------------
# GEOMETRIA, e por que esta e nao outra. O obstaculo fica DESLOCADO da rota e a
# tangencia: a rota global foi tracada no mapa estatico e o obstaculo nao estava
# nele, de sorte que seguir reto raspa a folga. Duas consequencias importam para a
# figura ser honesta. Primeira: as trajetorias DIVERGEM ao longo do horizonte e
# terminam separadas, porque um horizonte finito termina no meio da manobra -- a
# primeira versao desta figura as fazia reconvergir, que e o defeito que ela
# deveria evitar. Segunda: o obstaculo precisa estar fora do eixo, senao as
# amostras simetricas se cancelam e a media ponderada sai reta por cima dele.
X_OBST, Y_OBST, R_OBST = 5.6, 0.52, 0.52
MARGEM = 0.52          # folga desejada alem do raio
W_OBST, W_DESVIO = 30.0, 1.5
LAMBDA = 0.55          # temperatura da ponderacao exponencial


def rollouts(n=23, amp=2.6, comprimento=10.0, pontos=260):
    """Trajetorias que divergem a partir do robo, ao longo do horizonte."""
    x = np.linspace(0.0, comprimento, pontos)
    amps = np.linspace(-amp, amp, n)
    # curvatura aproximadamente constante: desvio cresce com o quadrado da
    # distancia percorrida e NAO retorna, que e o que um horizonte finito ve
    perfil = (x / comprimento) ** 2
    return x, amps, np.array([a * perfil for a in amps])


def custo(x, ys):
    """Custo de cada trajetoria: proximidade do obstaculo + desvio da rota."""
    d = np.sqrt((x - X_OBST) ** 2 + (ys - Y_OBST) ** 2)
    folga = d.min(axis=1)
    penal_obst = np.maximum(0.0, (R_OBST + MARGEM) - folga) ** 2
    penal_desvio = (ys ** 2).mean(axis=1)
    return W_OBST * penal_obst + W_DESVIO * penal_desvio


def fig_mppi(destino):
    x, amps, ys = rollouts()
    c = custo(x, ys)
    w = np.exp(-(c - c.min()) / LAMBDA)
    w /= w.sum()
    media = (w[:, None] * ys).sum(axis=0)     # o que o MPPI devolve

    fig, ax = plt.subplots(figsize=(7.1, 2.75))

    # rota do planejador global
    ax.plot(x, np.zeros_like(x), linestyle=(0, (1.2, 2.2)), color='#3b5f8a',
            linewidth=1.6, zorder=8)
    ax.text(3.15, 0.22, 'rota do planejador global', ha='center', va='bottom',
            fontsize=8.5, color='#3b5f8a', zorder=8)

    # obstaculo nao mapeado
    ax.add_patch(Circle((X_OBST, Y_OBST), R_OBST, facecolor='#cfcfcf',
                        edgecolor='#8a8a8a', linewidth=1.0, zorder=5))
    ax.annotate('obstáculo não mapeado',
                xy=(X_OBST, Y_OBST + R_OBST), xytext=(4.1, 2.35),
                fontsize=8.5, color='#5a5a5a', ha='center',
                arrowprops=dict(arrowstyle='-', color='#9e9e9e', linewidth=0.8))

    # trajetorias sorteadas, coloridas PELO CUSTO CALCULADO
    corte = np.percentile(c, 40)
    for yi, ci in zip(ys, c):
        if ci <= corte:
            ax.plot(x, yi, color=AZUL, linewidth=1.5, alpha=0.9, zorder=3)
        else:
            ax.plot(x, yi, color=CINZA, linewidth=0.9, alpha=0.75,
                    linestyle=(0, (4, 2.6)), zorder=1)

    # legenda das duas classes
    ax.plot([10.35, 10.95], [1.75, 1.75], color=CINZA, linewidth=0.9,
            linestyle=(0, (4, 2.6)), zorder=3)
    ax.text(11.1, 1.75, 'alto custo', fontsize=8.5, color='#6a6a6a',
            ha='left', va='center')
    ax.plot([10.35, 10.95], [1.08, 1.08], color=AZUL, linewidth=1.5, zorder=3)
    ax.text(11.1, 1.08, 'baixo custo', fontsize=8.5, color=AZUL,
            ha='left', va='center')
    ax.plot([10.35, 10.95], [0.41, 0.41], color=LARANJA, linewidth=2.6, zorder=3)
    ax.text(11.1, 0.41, 'comando', fontsize=8.5, color=LARANJA,
            ha='left', va='center')

    # o que o controlador devolve: a media ponderada
    ax.plot(x, media, color=LARANJA, linewidth=2.6, zorder=6)
    ax.add_patch(FancyArrowPatch((x[-16], media[-16]), (x[-1], media[-1]),
                                 arrowstyle='-|>', mutation_scale=15,
                                 linewidth=2.6, color=LARANJA, zorder=6))
    ax.annotate('comando aplicado: média das\ntrajetórias ponderada pelo custo',
                xy=(6.6, media[int(0.66 * len(x))]), xytext=(3.4, -2.72),
                fontsize=8.5, color=LARANJA, ha='center', linespacing=1.3,
                arrowprops=dict(arrowstyle='-', color=LARANJA, linewidth=0.9))

    # robo
    ax.add_patch(Circle((0, 0), 0.26, facecolor='#4a4a4a',
                        edgecolor='#2a2a2a', linewidth=1.0, zorder=7))
    ax.text(-0.10, 0.40, 'robô', ha='center', va='bottom', fontsize=8.5,
            color='#2a2a2a')

    # marca o fim do horizonte
    ax.plot([10.0, 10.0], [ys[0][-1] - 0.25, ys[-1][-1] + 0.25],
            color='#b0b0b0', linewidth=0.9, linestyle=(0, (2, 2)), zorder=1)
    ax.text(10.35, -1.62, 'fim do horizonte:\ndescarta e\nreplaneja a\ncada ciclo',
            ha='left', va='center', fontsize=8.5, color='#5a5a5a',
            style='italic', linespacing=1.3)

    ax.set_xlim(-0.75, 13.3)
    ax.set_ylim(-3.15, 2.80)
    ax.set_aspect('equal')
    ax.axis('off')

    fig.savefig(destino)
    plt.close(fig)
    return destino, c, w, corte, media


def main():
    out = (sys.argv[1] if len(sys.argv) > 1
           else os.path.expanduser('~/tese_ws/docs/tese/figuras'))
    if not os.path.isdir(out):
        sys.exit('ERRO: diretorio de saida nao existe: %s' % out)

    a = fig_shaping(os.path.join(out, 'fig_shaping.pdf'))
    print('escrito: %s' % a)

    b, c, w, corte, media = fig_mppi(os.path.join(out, 'fig_mppi.pdf'))
    print('escrito: %s' % b)
    print('  trajetorias: %d   corte de custo: %.2f' % (len(c), corte))
    print('  custo min=%.2f  max=%.2f   peso max=%.3f' % (c.min(), c.max(), w.max()))
    print('  baixo custo (azuis): %d   alto custo (cinzas): %d'
          % (int((c <= corte).sum()), int((c > corte).sum())))
    print('  media ponderada no obstaculo: y=%.2f (obstaculo em y=%.2f, raio %.2f)'
          % (media[int(0.56 * len(media))], Y_OBST, R_OBST))


if __name__ == '__main__':
    main()
