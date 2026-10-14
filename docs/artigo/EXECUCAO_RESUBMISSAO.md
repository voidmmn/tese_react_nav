# Guia de Execução — Resubmissão IEEE Access (Access-2026-46291)

**Rastreador de tarefas.** O *quê* e o *porquê* estão em `PLANO_RESUBMISSAO.md` (v4);
aqui fica a **ordem**, as **dependências** e o **status**. Atualizar o status aqui ao
concluir cada item.

**Última atualização:** 2026-10-13

---

## ONDE ESTAMOS

```
F0 checagens bloqueantes  ████████████ 100%  CONCLUÍDA
F1 decisões               ██████░░░░░░  50%  D1+D4 aprovadas; D2/D3 são de texto
F2 implementação          ██████████░░  83%  gate F2.6 APROVADO
F3 plano de análise       ██████████░░  85%  falta commit (F3.3)
F4 bateria noite 1        █░░░░░░░░░░░   1%  ← RODANDO (lançada 21:41)
F5 bateria noite 2        ░░░░░░░░░░░░   0%  falta F2.5 + F2.9
F6 análises retrospectivas██████░░░░░░  50%  F6.1/F6.2 feitos, F6.3 dispensado
F7 reanálise + figuras    ░░░░░░░░░░░░   0%
F8 reescrita              ░░░░░░░░░░░░   0%
F9 empacotamento          ░░░░░░░░░░░░   0%
```

**Próxima ação:** rodar a **noite 1** (`bash rodar_bateria_resub.sh noite1`, ~8,8 h,
70 runs). Em paralelo: implementar F2.5 (`conflict_marginal`) e F2.9 (ensaio d = R),
que a noite 2 exige, e avançar F8 (texto), que não depende de dado novo.

> ### ⚠ RESTRIÇÃO DE EXECUÇÃO — não editar runtime com bateria em curso
>
> `build/tese_nav/tese_nav` é **symlink** para `src/tese_nav/tese_nav`
> (colcon `--symlink-install`), então cada run lê o fonte **ao vivo**. Editar
> `anomaly_simulator.py`, `stay_alert_node.py`, `bellman_node.py`,
> `attraction_field.py` ou os launches durante uma bateria faz runs do **mesmo
> bloco** rodarem com **código diferente** — e é impossível saber depois quais.
> É a confusão entre versão de implementação e efeito do método que a crítica
> v3 §4 manda impedir.
>
> **Regra:** com bateria em curso, só mexer em (a) scripts de análise em
> `scripts/` que não são importados pelos nós, (b) `docs/`. F2.5 e F2.9 só
> depois da noite 1 terminar.

**Legenda de status:** `[ ]` pendente · `[~]` em andamento · `[x]` concluído ·
`[!]` bloqueado · `[-]` descartado

---

## F0 — Checagens bloqueantes · CONCLUÍDA (2026-10-13)

| id | tarefa | status | resultado |
|---|---|---|---|
| F0.1 | Aritmética do update: `dQ == α·δ + η·Φ` | `[x]` | exato (<1e-12) p/ η∈{0,.5,.8}, Φ∈{0,±.8,±1.2,2} |
| F0.2 | Série temporal do resíduo por η | `[x]` | E0: 1/3754 difere (float noise); E2/E3/E4: ~64%, magnitude ∝ η |
| F0.3 | Semântica da coluna do resíduo | `[x]` | média de \|α·δ+η·Φ\| em janela de 1 s — magnitude, agregada, não assinada |
| F0.4 | Instrumentos geométricos do `metrics_node` | `[x]` | verdade de terreno; TF map→base; borda, não tick; 0.5/2.0 não sobrescritos; `robot_radius=0.25` |
| F0.5 | Desacoplamento do keepout (estático) | `[x]` | `_emit_keepout` sem gate da camada reativa; tópico casa com `hazard_layer` |
| F0.6 | Desacoplamento do keepout (smoke `KOFsmoke`) | `[x]` | sobem só anomaly/metrics/mission; `KEEPOUT_FIRST` a 4.94 m; **folga 1.73 m ≈ RHM 1.71** |

**Conclusões que liberaram o resto:**

- **Nenhum resultado precisa ser recalculado.** O instrumento do resíduo é sadio; a
  igualdade `full = α·td` nos valores finais era efeito da janela final (Φ=0 no fim da
  missão). → **o reúso de E3/CONF/E5 não está comprometido** (resta só F2.6).
- **KOF funciona e já previu o resultado** (n=1): reproduz a folga do método completo
  sem camada reativa, inspeciona 0 anomalias, 50 s mais rápido.
- Artefatos do smoke em `results/_smoke_kof_20261013/` (fora de `results/` para não
  entrar nas análises).

---

## F1 — Decisões · 1 trava F4

| id | decisão | status | trava |
|---|---|---|---|
| **D1** | **Métrica de prioridade** (Eixo 3) | `[x]` **aprovada 2026-10-13** | — |
| D2 | `\history`/`\doi`: neutralizar? | `[ ]` | F8.1 |
| D3 | Título sem "Autonomous"? | `[ ]` | F8.1 |
| D4 | Rodar HEU/HEU-sel aceitando risco de empate | `[x]` aprovada junto de D1 | — |

### D1 — implementada em `scripts/metrica_prioridade.py`

Definição aprovada: prioridade pela **intensidade verdadeira dentro da mesma
modalidade**; desempate por **menor id**; relógio do **início da missão**;
**H = 400 s**; não inspecionado até H recebe **H no escore**, relatado em separado com
a proporção inspecionada até H.

**Refinamento que a implementação exigiu (item 6 da docstring).** Em `conflict` a
anomalia de maior intensidade acústica (id=5, 0.95) está **deliberadamente
co-localizada com o perigo**, e o comportamento **correto** é recuar e não
inspecioná-la. Sem correção, a métrica **puniria o comportamento correto**. Anomalias
co-localizadas com perigo (≤ 1.0 m, parametrizável) passaram a ser **excluídas do
conjunto prioritário** → em `conflict` a prioridade acústica vira id=2 (0.72). A
exclusão é impressa na saída, nunca silenciosa.

**Problema de relógio achado na validação (teria invalidado a métrica).** O
`timestamp` dos CSVs de métricas é tempo de **simulação** (`use_sim_time=true`), mas o
`time_log_s` da trilha de auditoria é **epoch**. Os dois não se somam — a 1ª versão
devolveu 0/10 inspecionados. Solução que **preserva o reúso**: mapa linear wall→sim
por run, ancorado em dois pontos recuperáveis de qualquer log, antigo ou novo —
`-> WP[0]` do `mission_node` (início) e `Missão COMPLETA` do `metrics_node` (fim) ↔
`max(mission_duration_s)`. O fator corrige a deriva de RTF, medida entre **0.967 e
1.000 e variável por run**: sem a correção, uma config que replaneja mais (mais CPU,
RTF menor) teria tempos inflados por artefato de host, não por comportamento.

**Primeiro resultado (dados existentes, retrospectivo):** o método inspeciona o alvo
prioritário **antes do APF** — térmico 240.8 s vs 269.7 s; acústico 283.9 s vs
324.8 s (medianas, 10/10 e 9/9). Em N2 (ruído alto) a censura aparece: 8/9 e 7/9.
É o critério independente que faltava para R2#3.

**D1 — proposta a aprovar ou ajustar** (de `PLANO_RESUBMISSAO.md` §4):

- prioridade pela **intensidade verdadeira dentro da mesma modalidade** (entre
  modalidades o peso de tipo — thermal 1.0, acoustic 1.2 — *é* a regra sob teste e não
  pode julgá-la);
- desempate por **menor id**;
- contagem desde o **início da missão**;
- **H = 400 s** (acima dos ~372 s do método em `route_hazard` e dos ~365 s da missão
  nominal; abaixo do timeout de 600 s);
- não inspecionado até H recebe **H no escore**, reportado **separadamente** junto da
  proporção inspecionada até H. O H imputado **não** é tempo observado de inspeção.

---

## F2 — Implementação · ~1,5 dia · não depende de decisão

| id | tarefa | arquivo | status |
|---|---|---|---|
| F2.1 | `selection_mode: {saliency, nearest}` | `anomaly_simulator.py` | `[x]` |
| F2.2 | `trigger_mode: {phi, range}` | `stay_alert_node.py` | `[x]` |
| F2.3 | Plumbing dos limiares de modalidade (eram hardcoded na dataclass) | `bellman_node.py`, launches | `[x]` |
| F2.4 | Plumbing do par `enter/exit_threshold` + `inspect_confirm_dist` | launches, runner | `[x]` |
| F2.5 | Cenário `conflict_marginal` (perigo marginal + **perda de observação**) | `anomaly_simulator.py` | `[ ]` |
| F2.6 | **Regressão de no-op:** 2 runs de `E3reg` c/ código novo vs E3 antigo | `rodar_bateria_resub.sh regressao` | `[x]` **APROVADO** |
| F2.7 | Script de re-scoring da confirmação (retrospectivo) | `scripts/rescore_confirmacao.py` | `[x]` |
| F2.8 | Blocos da resubmissão | `rodar_bateria_resub.sh` (novo) | `[x]` |
| F2.9 | Cenário do ensaio dirigido d = R (cruzamentos nos dois sentidos) | `anomaly_simulator.py` | `[ ]` |
| F2.10 | Métrica de prioridade (D1) | `scripts/metrica_prioridade.py` | `[x]` |
| F2.11 | Avaliador do gate de reúso | `scripts/gate_reuso.py` | `[x]` |
| F2.12 | Cenários extraídos para módulo sem ROS | `utils/scenarios.py` | `[x]` |

**F2.12 (refactor que a métrica exigiu):** as definições de cenário viviam em
`anomaly_simulator.py`, que importa `rclpy` no topo — logo nenhum script de análise
podia ler as intensidades verdadeiras sem ROS. Movidas para
`tese_nav/utils/scenarios.py` e **re-exportadas** pelo `anomaly_simulator`, então
`from tese_nav.anomaly_simulator import scenario_events` (usado por `metrics_node`,
`apf_node`, `qdriven_node`) segue válido. Verificado com o ambiente ROS carregado.
Agora há **fonte única da verdade** sobre posições e intensidades dos eventos.

### Como F2.1–F2.4 foram implementados

**Decisão de projeto central: tudo é default-preserving.** `selection_mode=saliency`,
`trigger_mode=phi`, `hazard_threshold=-1.0` (usa o default da dataclass),
`enter/exit=0.45/0.25`, `cfd=0.0` → o caminho do método proposto é idêntico ao
anterior. É isso que F2.6 verifica.

- **F2.1** `selection_mode` no `anomaly_simulator`: o laço de atração agora calcula um
  `score` — `|w_tipo·intensidade|` em `saliency`, `-dist` em `nearest`. **A publicação
  das intensidades é idêntica nos dois modos**, e o campo guarda o *máximo* sobre todas
  elas → **Φ no instante do disparo é o mesmo**. Logo HEU-sel é contraste de um fator
  no ponto de decisão. O efeito a jusante (anomalia diferente entra em `committed`,
  e committed deixa de alimentar o campo) está comentado no código para ser reportado.
- **F2.2** `trigger_mode` no `stay_alert_node`: extraí três predicados —
  `_attract_fires`, `_hazard_fires`, `_hazard_cleared`. Em `phi` reproduzem as
  expressões originais literalmente. Em `range` decidem por **frescor de pose**: o
  simulador publica `inspection_pose`/`retreat_pose` **só** para eventos dentro do
  alcance, então "pose fresca (≤1 s)" ≡ "evento no alcance" — detecção bruta, sem
  ponderação e sem usar a magnitude de Φ. Não precisou de tópico novo.
- **F2.3** limiares de modalidade: `bellman_node` passou a declarar
  `thermal/acoustic/hazard_threshold` e sobrescreve `self.field.thresholds` só quando
  o valor é ≥ 0. Antes eram defaults da dataclass `AttractionField`, inacessíveis.
- **F2.4** runner: colunas **10–16** (`sel trig hthr ent ext cfd`) com defaults que
  reproduzem a matriz antiga. Parsing validado sem rodar simulação.

### F2.6 — GATE APROVADO (2026-10-13)

`python3 src/tese_nav/scripts/gate_reuso.py results --novo E3reg --ref E3` → exit 0.

| | referência (E3, n=10) | novo (E3reg, n=2) |
|---|---|---|
| anomalies_unique / route_deviations / hazard_avoidances | {3} / {4} / {1} | {3} / {4} / {1} |
| timeouts / collisions / zone_violations / deferred | {0} / {0} / {0} / {0} | {0} / {0} / {0} / {0} |
| mission_duration_s | 361.67–366.68 | 362.65–364.00 |
| distance_traveled_m | 86.35–86.82 | 86.39–86.55 |
| min_hazard_distance_m | 4.81–4.92 | 4.86–4.92 |
| investigation_time_s | 34.00–36.40 | 34.40–35.00 |

**As 7 contagens discretas de comportamento são idênticas** e as 4 contínuas caem
dentro da faixa publicada. → **E3 / CONF / E5 reusáveis como "o método"**, poupando
~225 min. Bloco arquivado em `results/_gate_reuso_20261013/`.

Nota de método: o `gate_reuso.py` só admite runs com `Missão COMPLETA` no log — na
primeira leitura eu comparei com o run 2 ainda em escrita e obtive um falso
"reprovado". O script existe para que essa leitura precoce não se repita.

**Risco de proveniência registrado:** os args de launch `enter/exit_threshold` agora
**sombreiam** o `bellman_params.yaml`. Deixei os defaults idênticos (0.45/0.25) e pus
um aviso no YAML; o valor efetivo de cada run aparece no log do `stay_alert_node`
(`trigger=... enter=... exit=...`), o que dá rastreabilidade por run.

**F2.6 é o gate do reúso.** Se E3 com o código novo divergir do E3 antigo, a bateria do
método é refeita (+225 min). Rodar **antes** de F4.

**Parâmetros de referência para F2.5** (medidos): `CONFLICT_HAZARDS` usa intensidade
0.70 → `_haz = 1.5×0.70 = 1.05`, muito acima do `enter_threshold` 0.45. Para um perigo
*marginal* a intensidade precisa ficar em **~0.30–0.32** (`_haz ≈ 0.45–0.48`). E o
roteiro tem de incluir o perigo **saindo do alcance**, porque é o decaimento
(`_haz *= 0.85`/s) que cria a faixa "suprime mas não dispara retirada".

---

## F3 — Plano de análise escrito · depende de D1 · ~2 h

| id | tarefa | status |
|---|---|---|
| F3.1 | Documento consolidado: `PLANO_ANALISE_RESUB.md` | `[x]` |
| F3.2 | Tabela de reúso + condição de comparabilidade | `[x]` |
| F3.3 | Proveniência do código da noite 1 (MD5 + base git) | `[~]` checksums gravados; **falta commitar** |
| F3.4 | Rotular o que é **retrospectivo** | `[x]` §0 e §5 do plano de análise |

Chamar de **"plano de análise definido antes das novas execuções"**, nunca
"pré-registro" — não há registro formal em terceiros.

**Deslize de sequenciamento, registrado:** a noite 1 foi lançada (21:41) **antes** de
o documento F3 existir. As *declarações* precedem o lançamento e têm rastro
(cenários no `PLANO_RESUBMISSAO.md` v2 §4, revisado por terceiro; D1 aprovada,
implementada e validada em dados antigos; gate F2.6 aprovado) — mas o documento foi
redigido depois, e a §0 do `PLANO_ANALISE_RESUB.md` diz isso explicitamente em vez de
deixar implícito.

---

## F4 — Bateria noite 1 · ~6,3 h · depende de F2.6 + D1

| id | bloco | n | parede | status |
|---|---|---|---|---|
| F4.1 | `KOF` (ronda fixa + keepout, sem reativo) | 10 | ~75 min | `[ ]` |
| F4.2 | `HEU` × {default, conflict, adverse} | 30 | ~225 min | `[ ]` |
| F4.3 | `HEU-sel` × {default, conflict, adverse} | 30 | ~225 min | `[ ]` |

Método nos três cenários: **reúso** de E3 / CONF / E5 (não roda), condicionado a F2.6.

---

## F5 — Bateria noite 2 · ~8,2 h · depende de F2.3–F2.5

| id | bloco | n | parede | status |
|---|---|---|---|---|
| F5.1 | Limiar de modalidade do perigo {0.20, 0.30, 0.40} | 30 | ~225 min | `[ ]` |
| F5.2 | `conflict_marginal` (c/ perda de observação) | 10 | ~75 min | `[ ]` |
| F5.3 | Histerese (0.45,0.35) e (0.55,0.35) | 20 | ~150 min | `[ ]` |
| F5.4 | Ensaio dirigido d = R — **cruzamentos efetivos nos dois sentidos**, não tangente | 5 | ~40 min | `[ ]` |

**Total obrigatório F4+F5: 1.015 min = 16 h 55 min.** Bloco condicional de F6.3
(+150 min) levaria a 19 h 25 min / 3 noites.

---

## F6 — Análises retrospectivas · sem simulação

| id | tarefa | status |
|---|---|---|
| F6.1 | Re-scoring da confirmação {2.8, 3.3, 4.0} m em E3/N1/N2 | `[x]` **feito** |
| F6.2 | Distribuição da **distância no encerramento** (`robot_dist_m`) | `[x]` **feito** |
| F6.3 | *condicional:* instrumentar distância mínima + re-run E3/N2 (~150 min) | `[-]` **dispensado** — F6.1/F6.2 responderam |
| F6.4 | Recontagem de exclusões: **por tentativa** × **condicionado à partida** | `[ ]` |
| F6.5 | Bounds por denominador correto (25.9 / 28.3 / 31.2%) + escopo do que eles medem | `[ ]` |
| F6.6 | Tabela de tentativas/exclusões/motivos por grupo | `[ ]` |

### F6.1 + F6.2 — RESULTADO (2026-10-13, 0 runs novos)

Distância de **encerramento** da investigação e completude re-pontuada:

| cfg | dist. encerramento (mediana / min–max) | T=2.8 | T=3.3 | T=4.0 |
|---|---|---|---|---|
| E3 (sem ruído) | 2.23 / 2.21–2.24 | 10/10 | 10/10 | 10/10 |
| N1 (ruído moderado) | 2.31 / 1.92–3.07 | 6/10 | 10/10 | 10/10 |
| N2 (ruído alto) | 2.87 / 1.83–3.56 | 2/9 | **4/9** | **9/9** |

**Validação do pipeline:** em T=3.3 m o re-scoring reproduz **exatamente** o 4/9
publicado. O caminho de re-pontuação está correto.

**Resposta ao R2#5, em duas partes — e as duas são necessárias:**

1. **A métrica de completude é muito sensível ao critério.** Sob ruído alto, mover T
   de 3.3 para 4.0 m leva a completude de 4/9 a **9/9**. Ou seja, o robô *de fato se
   aproximou* das anomalias; parou a 2.9–3.6 m porque o ruído deslocou a posição
   percebida (e com ela a pose de inspeção), e o critério de 3.3 m recusou.
2. **Mas a qualidade física da aproximação degrada de verdade.** A distância de
   encerramento sai de 2.23 m (limpo) para **2.87 m de mediana e 3.56 m de máximo**
   sob ruído alto. A degradação **não é puro artefato de critério**.

→ Redação defensável: *a completude relatada é sensível ao critério de confirmação, e
a aproximação física também degrada sob ruído; os dois efeitos coexistem e são
reportados separadamente.* Isso é mais forte e mais honesto que a versão atual, que
atribui a degradação só à "confirmation rejection".

**F6.3 dispensado:** a distância de encerramento respondeu a pergunta. Poupa ~150 min
e evita a 3ª noite.

Valores já apurados: 160 tentadas, 154 válidas, 6 excluídas. APF 9, DHa 8, KOb 9,
N2 9, RHM 9, demais 10. As 6 exclusões são **todas** runs de 0 anomalias → excluí-las
**eleva** completude (RHM e APF 2.7→3.0; N2 2.1→2.33), e para **segurança** devem ser
excluídas (robô parado tem 0 contatos trivialmente).

---

## F7 — Reanálise e figuras

| id | tarefa | status |
|---|---|---|
| F7.1 | Painéis separados por cenário (nunca cruzar `default` × `route_hazard`) | `[ ]` |
| F7.2 | Tabela única do APF com IC + procedimento/esforço de tuning | `[ ]` |
| F7.3 | Fig. 7 com **sobreposição dos 4 η** (dados já existem; separação completa, U=100/100) | `[ ]` |
| F7.4 | Legenda da Fig. 7: banda = dispersão inter-run, **não** IC da média | `[ ]` |
| F7.5 | Contagem de cruzamentos de d=R × transições do FSM (de F5.4) | `[ ]` |
| F7.6 | Figuras novas: HEU/HEU-sel, sensibilidades | `[ ]` |

**F7.3 medido:** pico da média do resíduo 0.0965 (η=0) → 0.1894 → 0.2633 → 0.3712
(η=0.8); AUC mediana 0.0802 → 0.0877 → 0.0937 → 0.1066; **U = 100/100** de E0 contra
cada η>0 (Cliff's δ = 1.0). Enquadrar sem inflar: o resíduo contém ηΦ por definição,
então crescer com η é quase tautológico — o que a figura demonstra é que **o update
está implementado como especificado e é estável**, e nada sobre comportamento.

---

## F8 — Reescrita · pode começar junto de F2 (não depende de dado novo)

| id | tarefa | comentário atendido | status |
|---|---|---|---|
| F8.1 | Título, keywords (fora: Bellman, RL, **e risk-aware**), abstract, contribuições, conclusão | R3#1, R3-m1 | `[ ]` |
| F8.2 | Abstract: unidades e denominadores de "all of them" / 4-9 / 9-10 | R2#7 | `[ ]` |
| F8.3 | Abstract: bound na **mesma frase** da ausência de contatos; 1.71 m **dentro** da faixa de 2 m | R2#4 | `[ ]` |
| F8.4 | Atribuição do ganho de segurança ao keepout (com KOF) | R3#2 | `[ ]` |
| F8.5 | Nomenclatura: região de contato **definida operacionalmente**; 2 m = **limiar diagnóstico**, não requisito; calibração `robot_radius=0.25` | R3#2, v3§2 | `[ ]` |
| F8.6 | Rebaixar o update: apêndice, **sem lema e sem ponto fixo**; usar "Q não seleciona as ações executadas" | R2#1, R2#2 | `[ ]` |
| F8.7 | Circularidade do \|Φ\|: módulo colapsa atração/repulsão; bucket satura (bucket 3 cobre \|Φ\|∈[0.75,2.0]) | R2#10 | `[ ]` |
| F8.8 | Fronteira confirmatório × exploratório marcada por alegação | R2#4 | `[ ]` |
| F8.9 | Tab. 1: de matriz de features para **comparação de premissas** | R2-Q3 | `[ ]` |
| F8.10 | Related work: risk-aware/safety-filtered + keepout, **por lacuna argumentativa** | R3-Q4 | `[ ]` |
| F8.11 | Mover configs secundárias p/ apêndice (encurtar main text) | R3-m3 | `[ ]` |
| F8.12 | Proveniência: Φ do update lido no callback de odometria × Φ publicado no timer de 1 Hz | — | `[ ]` |
| F8.13 | §limitações apontando para os novos experimentos, não só declarando | R2-Q3 | `[ ]` |

---

## F9 — Empacotamento da submissão

| id | tarefa | status |
|---|---|---|
| F9.1 | **Confirmar no portal** o pacote de revisão anterior (qual slot juntou a carta) | `[ ]` |
| F9.2 | Carta-resposta no formato a/b/c por comentário | `[ ]` |
| F9.3 | Highlighted PDF (mudanças em amarelo) | `[ ]` |
| F9.4 | Clean PDF + fonte LaTeX | `[ ]` |
| F9.5 | Resposta **só** em *Author's Response Files* | `[ ]` |
| F9.6 | **Conferir o proof mesclado página por página antes do submit** | `[ ]` |

---

## Dependências críticas

```
F0 ✓ ──┬── F2 (implementação) ──┬── F2.6 regressão ──┬── F4 ── F7 ── F8 ── F9
        │                        │                     │
        └── F8.1-F8.13 (texto) ──┘                     └── F5 ──┘
D1 ────────────────────────────────── F3 ── F4.2/F4.3
F6 (retrospectivo, independente) ────────────── F7
```

**Caminho crítico:** D1 → F2 → F2.6 → F4 → F5 → F7 → F8 → F9.
**Gates que podem alargar o escopo:** F2.6 (reprovar = +225 min) e F6.1/F6.2
(dúvida = +150 min de F6.3).

---

## Riscos ativos

| risco | probabilidade | mitigação |
|---|---|---|
| HEU empata com o método no `default` | **alta** | cenários `conflict`/`adverse` já declarados em F3.1; relatar o empate — o R3 elogia franqueza com negativos |
| F2.6 reprova (parâmetros novos não são no-op) | baixa | implementar como default-preserving e testar antes de F4 |
| Degradação do WSL/DDS em bateria longa | **alta** (histórico: 6/160) | blocos de 10 com `deep_clean` entre eles, como no `rodar_bateria_blocos.sh` |
| `conflict_marginal` não produzir a faixa pretendida | média | parâmetros calculados em F2.5; validar com 1 smoke antes do bloco |
