# Proveniência da bateria (Access-2026-33687)

Manifesto de coleta dos 160 CSVs de métricas do pacote, para fixar qual versão de
código produziu cada lote e distinguir dados reaproveitados de dados recoletados.
A tag `v1.0-resubmission` é móvel entre rodadas; **este manifesto fixa a
correspondência por commit**, que a tag sozinha não garante.

## Commits por rodada

| Commit examinado | Papel | Dados de métricas |
|---|---|---|
| `c142b3fd5a3a8106d8a51fa9ccabbd08bb9948d8` | bateria de 160 (ensaio dirigido DHa/DHb inicial) | coleta rodada 3 |
| `12081a70ed645a78a348440e8d1623ac6678e781` | correções P0 + re-run E5/DHa/DHb | E5/DHa/DHb recoletados |
| `e7c04223c31695aee7a6074d6e67cfe32edd2e02` | esquema/escopo da auditoria + proveniência | **inalterados** vs anterior |
| atual (`git rev-parse v1.0-resubmission`) | Fig 5, TTC global, harmonização de texto, precisões de proveniência | **inalterados** vs anterior |

A tag `v1.0-resubmission` é móvel; identifique o pacote pelo **commit** (a linha
"atual" acima), não apenas pela tag.

Os hashes SHA-256 dos 160 CSVs estão em [`CHECKSUMS.sha256`](CHECKSUMS.sha256).

## Lotes de coleta

A coluna "Snapshot de referência" indica o commit que **contém e reproduz** o lote,
não uma prova de que todo o código desse commit foi executado na coleta original
(há reaproveitamento entre rodadas). Para os lotes reaproveitados, a justificativa
de compatibilidade está na seção final (0 abortos → caminho alterado não roda).

| Config | n | Coleta | Snapshot de referência (reproduz o lote) | Observação |
|---|---:|---|---|---|
| E3, CONF | 10 | 2026-09-08 | `c142b3f` (rodada 3) | reaproveitado |
| E0, E1, E2, E4, N1, N2, APF, RHM, RHB, KOa, KOb | 10 | 2026-09-09 | `c142b3f` (rodada 3) | reaproveitado |
| **E5** | 10 | 2026-09-10 | **`12081a7` (rodada 4)** | recoletado |
| **DHa** | 10 | 2026-09-10 | **`12081a7` (rodada 4)** | recoletado |
| **DHb** | 10 | 2026-09-10 | **`12081a7` (rodada 4)** | recoletado |

### Dados substituídos (E5/DHa/DHb antigos)

A coleta antiga de E5/DHa/DHb (E5 de 2026-09-09; DHa/DHb de 2026-09-10 manhã) foi
**substituída** pela recoleta sob o código corrigido. Os arquivos anteriores são
identificáveis publicamente **no commit da 3ª rodada `c142b3f`**, sob os mesmos
caminhos `results/metrics_{E5,DHa,DHb}_*.csv` daquele snapshot (por exemplo,
`git show c142b3f -- results/metrics_E5_20260909_*.csv`). Uma cópia local também
foi arquivada em `results/_pre_rerun_P0/`, mas essa pasta **não** integra a árvore
versionada pública; para auditoria, use os caminhos do commit `c142b3f`.

## Sementes e reprodutibilidade

- `run_seed` = índice da repetição (1–10) de cada config, passado ao launch e
  **gravado em cada CSV** (métrica `run_seed`) — chave para casar CSV, log de
  execução (`launch_<CFG>_r<seed>.log`) e trilha de auditoria (`audit_trail.csv`).
- Runner: `rodar_bateria_blocos.sh` (matriz completa) / `rodar_experimentos.sh`
  (subconjunto por `EXPERIMENTS`). Timeout de parede 600 s por execução.

## Justificativa do reaproveitamento (rodada 4 → 5)

As correções da 4ª rodada alteraram o tratamento de falhas de navegação e a
ativação do perigo dinâmico. Os 13 configs reaproveitados registram **zero**
abortos, cancelamentos e rejeições de navegação (colunas `nav_aborted`,
`nav_canceled`, `nav_rejected` = 0 em todas as execuções válidas) e não usam o
cenário `dyn_hazard`; portanto o caminho de código alterado **nunca é exercitado**
neles e suas métricas finais são idênticas sob qualquer das versões. É uma
identidade verificável a partir dos próprios contadores, não uma suposição. Só
E5, DHa e DHb — os cenários que exercitam esses caminhos — foram recoletados.
