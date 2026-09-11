# Proveniência da bateria (Access-2026-33687)

Manifesto de coleta dos 160 CSVs de métricas do pacote, para fixar qual versão de
código produziu cada lote e distinguir dados reaproveitados de dados recoletados.
A tag `v1.0-resubmission` é móvel entre rodadas; **este manifesto fixa a
correspondência por commit**, que a tag sozinha não garante.

## Commits por rodada

| Rodada | Commit | Papel |
|---|---|---|
| 3ª | `c142b3fd5a3a8106d8a51fa9ccabbd08bb9948d8` | bateria de 160 (ensaio dirigido DHa/DHb inicial) |
| 4ª | `12081a70ed645a78a348440e8d1623ac6678e781` | correções P0 + re-run E5/DHa/DHb |
| 5ª (esta) | ver `git rev-parse v1.0-resubmission` | correções direcionadas (auditoria, totais, texto); **dados de métricas inalterados** vs 4ª |

Os hashes SHA-256 dos 160 CSVs estão em [`CHECKSUMS.sha256`](CHECKSUMS.sha256).

## Lotes de coleta

| Config | n | Coleta | Versão de código da coleta | Observação |
|---|---:|---|---|---|
| E3, CONF | 10 | 2026-09-08 | rodada 3 (`c142b3f`) | reaproveitado |
| E0, E1, E2, E4, E5*, N1, N2, APF, RHM, RHB, KOa, KOb | 10 | 2026-09-09 | rodada 3 (`c142b3f`) | reaproveitado (exceto E5) |
| **E5** | 10 | 2026-09-10 | **rodada 4 (`12081a7`)** | recoletado |
| **DHa** | 10 | 2026-09-10 | **rodada 4 (`12081a7`)** | recoletado |
| **DHb** | 10 | 2026-09-10 | **rodada 4 (`12081a7`)** | recoletado |

`*` E5 aparece nas duas datas apenas porque a coleta antiga (2026-09-09) foi
**substituída**; os CSVs antigos de E5/DHa/DHb estão preservados, fora da árvore
versionada, em `results/_pre_rerun_P0/`.

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
