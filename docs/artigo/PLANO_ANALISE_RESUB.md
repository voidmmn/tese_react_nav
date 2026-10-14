# Plano de Análise — Resubmissão IEEE Access (Access-2026-46291)

**Documento F3 do guia de execução.** Consolida cenários, contrastes, métricas e
regras de censura **declarados antes das novas execuções**, mais a proveniência do
código que as produziu.

## 0. Status honesto deste documento

Este documento foi **redigido em 2026-10-13, após o lançamento da bateria da noite 1**
(21:41). Não se afirma o contrário.

O que **de fato precede** as execuções, com rastro verificável:

| declaração | onde foi feita antes | evidência |
|---|---|---|
| cenários `default`, `conflict`, `adverse` para método × HEU × HEU-sel | `PLANO_RESUBMISSAO.md` v2 §4 ("Cenários definidos no plano de análise") | revisado por terceiro em `Avaliacao_Plano_Resubmissao_v2/v3`, que cobraram e aprovaram essa mudança |
| contraste de um fator (HEU-sel) separado do supervisor completo (HEU) | `PLANO_RESUBMISSAO.md` v2 §4 | idem |
| métrica de prioridade e regra de censura (D1) | aprovada antes do lançamento; implementada e **validada em dados antigos** antes | `scripts/metrica_prioridade.py`, saída conferida contra E3/APF/N2 |
| reúso de E3/CONF/E5 condicionado a gate | `PLANO_RESUBMISSAO.md` v4 §4 | `scripts/gate_reuso.py`, **aprovado** antes do lançamento |

**Não é pré-registro.** Não há registro em repositório de terceiros. É um plano de
análise cujas decisões antecedem as execuções, com o rastro acima — e esta seção
existe para que ninguém leia mais do que isso.

**Análises retrospectivas** (sobre dados já existentes, planejadas agora): re-scoring
da confirmação (F6.1/F6.2) e recontagem de exclusões (F6.4–F6.6). Rotuladas como
retrospectivas onde aparecerem.

## 1. Proveniência do código — bateria da noite 1

Base git: `8ed4868` **+ modificações não commitadas** (a bateria roda contra o fonte
via `colcon --symlink-install`). Checksums MD5 do runtime no instante do lançamento:

```
823d8796200c26647233bb56417774e4  tese_nav/anomaly_simulator.py
e1ba2159d3bb2a335285f550fd56892f  tese_nav/stay_alert_node.py
396945f2c84db561cbe5f9ef29aa7dfe  tese_nav/bellman_node.py
f538f09c7607c9b1cfadf57f1e7e71cb  tese_nav/utils/attraction_field.py
f6c9145bb4bc8e33192589ff3efeaa77  tese_nav/utils/scenarios.py
4c777940edd69152ef6ab3d1c1275dd8  tese_nav/utils/q_table.py
e1f3521e573e94ba373e93608cbb6714  launch/stay_alert.launch.py
a87807f746b12f81e0d06ccd4b0891ec  launch/experimento.launch.py
d4633ec77735d6cd6b543f586c89ded8  config/bellman_params.yaml
904c8a5098e220528dcc22517dd921da  config/nav2_params_sim.yaml
98df39223cbb4bac82722c96e8291d02  scripts/rodar_experimentos.sh
a59ecdf656f1b56f77afbf40d1758bf4  rodar_bateria_resub.sh
```

**Pendência:** commitar este estado para dar um identificador estável ao grupo de
dados da noite 1. Até o commit, os checksums acima são a âncora.

## 2. Tabela de reúso de dados (F3.2)

| comparação | dados do método | dados novos | condição de comparabilidade |
|---|---|---|---|
| método × HEU × HEU-sel, por cenário | **reúso:** E3 (default), CONF (conflict), E5 (adverse) | HEUd/HEUc/HEUa, HEUseld/HEUselc/HEUsela | defaults novos são no-op — **verificado por F2.6** |
| RHM/RHB/KOa/KOb × KOF | **reúso:** RHM, RHB, KOa, KOb | KOF | mesmo `route_hazard`, mesmos instrumentos (0.5 m / 2.0 m) |
| sensibilidades | **referência:** E3 (histerese), HAZ30 (limiar) | HAZ20/HAZ40, HYSnar/HYSoff | alteração deliberada de um fator por bloco |

**Gate que licenciou o reúso (F2.6, aprovado):** 2 runs de `E3reg` com o código novo
reproduziram E3 — as 7 contagens discretas idênticas (`{3} {4} {1} {0} {0} {0} {0}`) e
as 4 contínuas dentro da faixa publicada. Bloco em `results/_gate_reuso_20261013/`.

## 3. Cenários e contrastes

| bloco | cenário | sel | trig | o que isola |
|---|---|---|---|---|
| E3 / CONF / E5 (reúso) | default / conflict / adverse | saliency | phi | o método |
| HEUd / HEUc / HEUa | default / conflict / adverse | nearest | **range** | supervisor genérico completo (R2#3) |
| HEUseld / HEUselc / HEUsela | default / conflict / adverse | **nearest** | phi | **só** o critério de seleção |
| KOF | route_hazard | — (sa=off) | — | só a função de segurança (R3#2) |
| HAZ20 / HAZ30 / HAZ40 | conflict | saliency | phi | limiar de **modalidade** = precedência (R2#6) |
| HYSnar / HYSoff | default | saliency | phi | largura × posição da histerese (R3#3) |

**Caveat de acoplamento de HEU-sel, a reportar:** trocar o argmax **não** muda Φ no
instante do disparo (o simulador publica a intensidade de todas as anomalias no
alcance e o campo guarda o máximo). Mas muda qual anomalia entra em `committed`, e
committed deixa de alimentar o campo → há efeito **a jusante** na trajetória temporal
de Φ. Não descrever o contraste como "apenas ordem de atendimento".

**Histerese — os três pares separam posição de largura:**
referência (0.45, 0.25) largura 0.20 · estreita (0.45, 0.35) largura 0.10 ·
deslocada (0.55, 0.35) largura 0.20.

## 4. Métrica de prioridade (D1) e censura

- evento prioritário = **maior intensidade verdadeira dentro da mesma modalidade**
  (entre modalidades o peso de tipo — thermal 1.0, acoustic 1.2 — *é* a regra sob
  teste e não pode julgá-la);
- desempate: **menor id**;
- relógio: do **início da missão** (`-> WP[0]` do `mission_node`);
- horizonte **H = 400 s**;
- não inspecionado até H → **H no escore**, relatado **separadamente** com a proporção
  inspecionada até H. O H imputado **não** é tempo observado de inspeção;
- anomalias **co-localizadas com perigo** (≤ 1.0 m) são **excluídas** do conjunto
  prioritário — em `conflict` a de maior intensidade acústica (id=5, 0.95) é
  deliberadamente co-localizada e o comportamento correto é recuar, logo sem a
  exclusão a métrica puniria o acerto.

**Correção de relógio, necessária e declarada:** o `timestamp` dos CSVs é tempo de
**simulação**; o `time_log_s` da trilha é **epoch**. Converte-se wall→sim por run com
fator `max(mission_duration_s) / (t_COMPLETA − t_WP[0])`. A RTF medida fica entre
**0.967 e 1.000 e varia por run**: sem a correção, uma config que replaneja mais
(mais CPU, RTF menor) teria tempos inflados por artefato de host.

## 5. Exclusões e famílias de inferência

- **Exclusão de run:** sem `Missão COMPLETA` no log **ou** `distance_traveled_m ≤ 1 m`
  (falha de partida).
- Reportar **as duas leituras**: (a) por **tentativa de missão**, incluindo falhas de
  partida; (b) **condicionado à inicialização bem-sucedida**. A direção do ajuste é
  **oposta** entre completude e segurança — um run em que o robô não se moveu tem 0
  contatos trivialmente e não pode aumentar a evidência de navegação sem contato.
- Não pressupor independência entre falha de inicialização e configuração.
- **Confirmatório:** método × HEU e método × HEU-sel no `default`, e KOF × KOa em
  `route_hazard`, com correção de Holm na família.
- **Exploratório:** `conflict`, `adverse`, sensibilidades e todas as análises
  retrospectivas. Rotular por alegação, não só por tabela.

## 6. Bounds de segurança

Bound exato unilateral 95% para zero ocorrências do evento contado:
**n=10 → 25.9%**, **n=9 → 28.3%**, **n=8 → 31.2%**. Usar o denominador do grupo.
Escopo: probabilidade **por execução do evento operacionalmente contado**, nas
condições estudadas — **não** limite geral de falha de segurança, colisão física ou
operação em subestação real.
