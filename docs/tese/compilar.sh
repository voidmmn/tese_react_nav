#!/bin/bash
# Compila a tese: 3 passadas de pdflatex + bibtex. Uso: ./compilar.sh
set -e
cd "$(dirname "$0")"
pdflatex -interaction=nonstopmode main_ppgee_ufu.tex >/dev/null 2>&1 || true
bibtex main_ppgee_ufu >/dev/null 2>&1 || true
pdflatex -interaction=nonstopmode main_ppgee_ufu.tex >/dev/null 2>&1 || true
pdflatex -interaction=nonstopmode main_ppgee_ufu.tex >/dev/null 2>&1 || true
if [ -f main_ppgee_ufu.pdf ]; then
  cp main_ppgee_ufu.pdf Tese_Milton_Miranda_Neto.pdf
  echo "OK  paginas=$(pdfinfo main_ppgee_ufu.pdf | awk '/^Pages/{print $2}')  erros=$(grep -ac '^! ' main_ppgee_ufu.log || echo 0)"
  echo "citacoes indefinidas:"; grep -aoP "Citation \`\K[^']+" main_ppgee_ufu.log | sort -u
else
  echo "FALHOU"; grep -a -m8 '^! ' main_ppgee_ufu.log
fi
