#!/usr/bin/env python3
"""Marca em amarelo, no PDF NOVO, o texto que mudou em relacao ao PDF ANTIGO.

Diff no nivel de PALAVRA (nao de linha): as quebras de linha e de coluna mudam
entre as duas versoes, entao um diff de linhas marcaria paragrafos inteiros por
causa de refluxo. Palavras sao reunidas em corridas contiguas na mesma linha
para que cada marca cubra uma frase, nao palavra a palavra.

Uso: destacar.py ANTIGO.pdf NOVO.pdf SAIDA.pdf
"""
import re
import sys
import difflib
import pymupdf


def norm(w):
    """Forma de comparacao: sem pontuacao de borda, sem caixa, sem ligaduras."""
    w = w.replace('ﬁ', 'fi').replace('ﬂ', 'fl')
    w = w.replace('’', "'").replace('–', '-').replace('—', '-')
    return re.sub(r'^\W+|\W+$', '', w).lower()


def dehyphenate(words):
    """Junta 'work-' + 'ing' quebrados por fim de linha.

    Sem isto, uma palavra que quebra em pontos diferentes nas duas versoes
    aparece como diferenca, e o refluxo de 16 para 24 paginas muda quase todas.
    """
    out = []
    i = 0
    while i < len(words):
        w = words[i]
        txt = w[4]
        if (txt.endswith('-') and i + 1 < len(words)
                and words[i + 1][4][:1].islower()
                and abs(words[i + 1][3] - w[3]) > 1):       # linha seguinte
            nxt = words[i + 1]
            merged = (w[0], w[1], w[2], w[3], txt[:-1] + nxt[4],
                      w[5], w[6], w[7])
            out.append((merged, [w, nxt]))                   # texto, rects fonte
            i += 2
        else:
            out.append((w, [w]))
            i += 1
    return out


# Abaixo disto o texto esta DENTRO de uma figura (rotulos de eixo, ticks,
# legendas do grafico). Medido neste manuscrito: corpo 10 pt, legendas de
# figura e tabela 7.0-8.0 pt, interior de figura 4.4-6.7 pt.
FIG_PT = 6.9


def small_text_boxes(page):
    """Bboxes dos spans com fonte de figura, para excluir seu texto do diff.

    Sem isto, rotulos de figuras que NAO mudaram (os ticks do world_map, por
    exemplo) aparecem como alteracao: o texto da figura ocupa posicao diferente
    no fluxo de leitura entre as duas versoes e o alinhamento desliza. Marcar
    tick a tick tambem nao informa nada -- o que mudou numa figura e dito na
    legenda, que tem 7 pt e continua entrando no diff.
    """
    boxes = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for sp in l["spans"]:
                if sp["size"] < FIG_PT and sp["text"].strip():
                    boxes.append(pymupdf.Rect(sp["bbox"]))
    return boxes


def load(path, with_rects):
    """(tokens normalizados, [(pagina, [rects])]) em ordem de leitura."""
    doc = pymupdf.open(path)
    toks, meta = [], []
    for pno, page in enumerate(doc):
        figs = small_text_boxes(page)
        ws = page.get_text("words")            # x0,y0,x1,y1,word,block,line,no
        ws.sort(key=lambda w: (w[5], w[6], w[7]))
        for merged, srcs in dehyphenate(ws):
            n = norm(merged[4])
            if not n:
                continue
            r0 = pymupdf.Rect(srcs[0][:4])
            centro = pymupdf.Point((r0.x0 + r0.x1) / 2, (r0.y0 + r0.y1) / 2)
            if any(centro in f for f in figs):
                continue
            toks.append(n)
            if with_rects:
                meta.append((pno, [pymupdf.Rect(s[:4]) for s in srcs]))
    if not with_rects:
        doc.close()
    return (toks, meta, doc) if with_rects else (toks, None, None)


def main():
    old_p, new_p, out_p = sys.argv[1], sys.argv[2], sys.argv[3]
    old_toks, _, _ = load(old_p, False)
    new_toks, meta, doc = load(new_p, True)

    sm = difflib.SequenceMatcher(None, old_toks, new_toks, autojunk=False)
    changed = set()
    for tag, _i1, _i2, j1, j2 in sm.get_opcodes():
        if tag in ('replace', 'insert'):
            changed.update(range(j1, j2))

    # agrupa indices contiguos na mesma pagina e mesma linha -> um retangulo
    marks, run = [], []
    for idx in sorted(changed):
        if run and idx == run[-1] + 1 and meta[idx][0] == meta[run[-1]][0] \
                and abs(meta[idx][1][0].y0 - meta[run[-1]][1][0].y0) < 2:
            run.append(idx)
        else:
            if run:
                marks.append(run)
            run = [idx]
    if run:
        marks.append(run)

    # as paginas precisam ficar vivas enquanto a anotacao e configurada: um
    # doc[pno] temporario e coletado e a anotacao perde o vinculo
    pages = [doc[i] for i in range(doc.page_count)]
    n_annot = 0
    for run in marks:
        page = pages[meta[run[0]][0]]
        rects = [r for i in run for r in meta[i][1]]
        # NAO unir tudo num retangulo so. Uma palavra hifenizada no fim de
        # COLUNA tem os dois pedacos em cantos opostos da pagina ("mani-" no
        # rodape da esquerda, "fest" no topo da direita); a uniao viraria uma
        # caixa do tamanho da pagina. Agrupa por linha (mesmo y) e une dentro
        # de cada linha -- o caso normal da uma caixa, o caso partido da duas.
        rects.sort(key=lambda r: (round(r.y0, 1), r.x0))
        linhas = []
        for r in rects:
            if linhas and abs(r.y0 - linhas[-1][0].y0) < 2:
                linhas[-1].append(r)
            else:
                linhas.append([r])
        for grupo in linhas:
            rect = grupo[0]
            for r in grupo[1:]:
                rect |= r
            rect &= page.rect                     # nunca fora da pagina
            if rect.is_empty or rect.height > 40:  # guarda contra uniao absurda
                continue
            # texto ROTACIONADO (rotulo de eixo de figura) tem retangulo mais
            # alto que largo; marca-lo produz manchas verticais em vez de grifo,
            # e marcar palavra a palavra dentro de um grafico nao informa nada:
            # o que mudou e a figura inteira, dita na legenda.
            if rect.height > rect.width and rect.height > 12:
                continue
            a = page.add_highlight_annot(rect)
            a.set_colors(stroke=(1, 0.92, 0.23))  # amarelo
            a.set_opacity(0.4)
            a.update()
            n_annot += 1

    doc.save(out_p, garbage=3, deflate=True)
    pct = 100.0 * len(changed) / max(1, len(new_toks))
    print(f"palavras antigo : {len(old_toks)}")
    print(f"palavras novo   : {len(new_toks)}")
    print(f"marcadas        : {len(changed)} ({pct:.1f}% do novo)")
    print(f"anotacoes       : {n_annot}")
    print(f"saida           : {out_p}")


if __name__ == '__main__':
    main()
