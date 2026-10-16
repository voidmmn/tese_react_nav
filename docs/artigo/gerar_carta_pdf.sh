#!/usr/bin/env bash
# Gera o PDF da carta-resposta a partir do markdown.
#
# O portal da IEEE Access pede a resposta como arquivo separado, no slot
# "Author's Response Files" -- NAO anexada ao manuscrito (foi a juncao indevida
# que gerou o R3-m3 da rodada anterior).
#
# XeLaTeX, nao pdflatex: a carta usa grego (Phi, eta, delta, alpha), sobrescritos
# (10^-4), subscritos e simbolos matematicos que o pdflatex nao compoe sem
# pacote a pacote. A conferencia no fim valida que nenhum caiu.
set -euo pipefail
cd "$(dirname "$0")"
MD=response_to_reviewers_46291.md
PDF=response_to_reviewers_46291.pdf

pandoc "$MD" -o "$PDF" \
  --pdf-engine=xelatex -H carta_preambulo.tex \
  -V colorlinks=true -V linkcolor=accessblue -V urlcolor=accessblue

echo "paginas: $(pdfinfo "$PDF" | awk '/^Pages/{print $2}')"
echo "conferindo caracteres especiais (md vs pdf):"
TXT=$(mktemp); pdftotext "$PDF" "$TXT"
for c in Φ η δ α ≈ ≤ → × ⁻ § ₑ; do
  a=$(grep -o "$c" "$MD" | wc -l); b=$(grep -o "$c" "$TXT" | wc -l)
  [ "$a" = "$b" ] && s=ok || s="DIVERGE"
  printf '  %-3s %3s -> %3s  %s\n' "$c" "$a" "$b" "$s"
done
rm -f "$TXT"
