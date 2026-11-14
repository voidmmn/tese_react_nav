#!/usr/bin/env bash
# ===========================================================================
# Pacote de reprodutibilidade da tese -- 14/11/2026
#
# Alternativa imediata a publicacao da
# etiqueta, um pacote anexado contendo codigo, configuracoes, manifesto,
# resultados, logs e scripts. Este script o monta.
#
# Os diretorios de descarte somam ~160 MB e NAO entram inteiros: entra o
# manifesto com caminho, tamanho e sha256 de cada arquivo deles, que e o que
# permite reconciliar as contagens de lancamento sem o volume. Declarado no
# README do pacote.
#
# Uso: bash empacotar_reprodutibilidade.sh [destino.tar.gz]
# ===========================================================================
set -euo pipefail
WS="$HOME/tese_ws"
OUT="${1:-$WS/pacote_reprodutibilidade_$(date +%Y%m%d).tar.gz}"
TMP="$(mktemp -d)"
P="$TMP/pacote_reprodutibilidade"
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$P"/{codigo,resultados,analise,descartes,verificacao do decaimento}

# --- codigo, configuracoes e launch -------------------------------------
cp -r "$WS/src/tese_nav" "$P/codigo/"
rm -rf "$P/codigo/tese_nav/scripts/__pycache__"
for f in rodar_bateria_resub.sh rodar_bateria_blocos.sh run_bateria_noturna.sh \
         rodar_verificacao_r201.sh; do
  [ -f "$WS/$f" ] && cp "$WS/$f" "$P/codigo/"
done

# --- resultados analisados: so os 320 da matriz -------------------------
cd "$WS/results"
for f in launch_*.log metrics_*.csv; do
  case "$f" in
    launch_CMw_*|launch_CMs_*|launch_E3w_*|launch_E3s_*|launch_HEUw_*|launch_HEUs_*) continue;;
    metrics_CMw_*|metrics_CMs_*|metrics_E3w_*|metrics_E3s_*|metrics_HEUw_*|metrics_HEUs_*) continue;;
  esac
  cp "$f" "$P/resultados/" 2>/dev/null || true
done
for f in audit_trail.csv CHECKSUMS.sha256 manifesto_execucoes.csv \
         familia_confirmatoria.csv qdriven_exploratorio.csv \
         reconciliacao_lancamentos.csv resumo_experimentos.csv; do
  [ -f "$f" ] && cp "$f" "$P/resultados/"
done
cp tabelas/* "$P/resultados/" 2>/dev/null || true

# --- verificacao direcionada de verificacao do decaimento -----------------------------------
for f in launch_CMw_* launch_CMs_* launch_E3w_* launch_E3s_* launch_HEUw_* launch_HEUs_* \
         metrics_CMw_* metrics_CMs_* metrics_E3w_* metrics_E3s_* metrics_HEUw_* metrics_HEUs_* \
         verificacao_r201.log; do
  [ -e "$f" ] && cp "$f" "$P/verificacao_decaimento/" 2>/dev/null || true
done

# --- analise -------------------------------------------------------------
cp "$WS"/src/tese_nav/scripts/*.py "$P/analise/" 2>/dev/null || true
rm -rf "$P/analise/__pycache__"

# --- descartes: manifesto, nao os arquivos ------------------------------
{
  echo "sha256,tamanho_bytes,caminho"
  for d in _*/; do
    find "$d" -type f -print0 | sort -z | while IFS= read -r -d '' f; do
      printf '%s,%s,%s\n' "$(sha256sum "$f" | cut -d' ' -f1)" \
                          "$(stat -c%s "$f")" "$f"
    done
  done
} > "$P/descartes/MANIFESTO_DESCARTES.csv"

# --- README --------------------------------------------------------------
COMMIT=$(git -C "$WS" rev-parse HEAD)
cat > "$P/README.md" <<EOF
# Pacote de reprodutibilidade --- tese de Milton Miranda Neto

Gerado em $(date -Iseconds) a partir do *commit* \`$COMMIT\`.

## O que ha aqui

| Diretorio | Conteudo |
|---|---|
| \`codigo/tese_nav/\` | pacote ROS 2 completo: nos, *launch*, configuracoes, *scripts* |
| \`codigo/rodar_*.sh\` | executores das baterias, incluindo a verificacao de verificacao do decaimento |
| \`resultados/\` | as **320** execucoes analisadas: um CSV e um log de lancamento por execucao, mais a trilha de auditoria, o manifesto, as somas de verificacao e as tabelas geradas |
| \`verificacao_decaimento/\` | verificacao direcionada do decaimento temporal: execucoes sob relogio de parede e sob relogio simulado |
| \`analise/\` | todos os *scripts* de analise; dados os CSVs, regeneram cada numero relatado |
| \`descartes/\` | **manifesto** (caminho, tamanho, sha256) dos lancamentos excluidos |

## Reconciliacao dos lancamentos

\`resultados/reconciliacao_lancamentos.csv\` reconcilia **595** lancamentos
registrados com as **320** execucoes analisadas, diretorio por diretorio e
rotulo por rotulo, com origem e criterio de exclusao. Nenhum diretorio fica sem
classificacao.

Os arquivos dos descartes somam cerca de 160 MB e **nao** vao neste pacote. Vai
o manifesto com o sha256 de cada um, que permite conferir as contagens e a
integridade; os arquivos estao disponiveis sob solicitacao.

## Limitacoes declaradas

1. **Nao ha *commit* por execucao nas baterias anteriores a 13/11/2026.** O
   executor nao o gravava. A informacao nao foi reconstruida: seria conjetura
   apresentada como registro. A coluna existe no manifesto e esta **vazia** para
   essas baterias. De 13/11/2026 em diante o executor grava \`commit=<sha>\`, com
   sufixo \`+sujo\` quando a arvore esta modificada.
2. **A reexecucao nao reproduz os mesmos numeros, e nao se pode afirmar que
   amostre a mesma distribuicao.** A guarda do decaimento compara instantes de
   relogio de **parede** enquanto os temporizadores correm em tempo simulado, de
   modo que a dinamica efetiva do campo depende de hardware, carga e
   escalonamento. O que e reproduzivel por construcao e a **analise**: dados os
   mesmos CSVs, todo numero relatado e regenerado bit a bit.
3. **A bateria noturna de 01/09/2026 perdeu os logs de lancamento**; restam os
   CSVs. E a unica lacuna de registro entre os descartes.
4. **As somas de verificacao comprovam integridade dos arquivos deste pacote.**
   Nao comprovam, sozinhas, qual versao do codigo produziu cada trajetoria ---
   e por isso a limitacao 1 esta declarada.
EOF

# --- manifesto do proprio pacote ----------------------------------------
cd "$P"
find . -type f ! -name MANIFEST.sha256 -print0 | sort -z \
  | xargs -0 sha256sum > MANIFEST.sha256

cd "$TMP"
tar czf "$OUT" pacote_reprodutibilidade
echo "pacote: $OUT"
echo "tamanho: $(du -h "$OUT" | cut -f1)"
echo "arquivos: $(tar tzf "$OUT" | wc -l)"
echo "sha256: $(sha256sum "$OUT" | cut -d' ' -f1)"
