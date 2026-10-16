# Plano de Resubmissão — IEEE Access (Access-2026-46291) — v4

**Decisão do editor:** reject-and-resubmit (processo binário). **Uma única** chance de
resubmeter; se o Associate Editor ainda tiver objeção técnica substancial, rejeição
definitiva sem novo round.

**Revisores:** R1 aprovou sem ações. R2 (10 comentários) e R3 (3 majors + 3 minors)
convergem no mesmo eixo central.

**Enquadramento escolhido:** rebaixar Bellman/RL no artigo, manter a arquitetura de
duas camadas como contribuição, corrigir a atribuição causal dos ganhos de segurança.

**v2** incorporou `Avaliacao_Plano_Resubmissao_IEEE_Access.md` + auditoria de
código/dados. **v3** incorpora `Avaliacao_Plano_Resubmissao_v2_IEEE_Access.md` +
segunda auditoria. Mudanças acumuladas:

| | v1 | v2 | v3 |
|---|---|---|---|
| QD/QD0 (Q comportamental) | apêndice | **fora do artigo** | — |
| Lema de perturbação limitada | obrigatório | retirado | — |
| Ponto fixo descritivo | — | opcional | **retirado** |
| HEU | 1 config | 2 configs | + caveat de acoplamento |
| Cenários de HEU | condicionais | pré-registrados | **"plano de análise prévio"** |
| Confirmação | 30 runs | 0 runs (re-scoring) | + limite da medida física |
| Perigo marginal | `enter_threshold` | limiar de modalidade | **+ decaimento/perda de observação** |
| Histerese | par solto | 3 pares | **3 pares que separam posição × largura** |
| KOF | "empata com RHM" | TOST obrigatório | **TOST só se houver margem justificada** |
| Bound de segurança | ~26% | 25.9/28.3/31.2% | **+ dois instrumentos (0.5 m × 2.0 m)** |
| Exclusões | — | "não enviesa RHM×APF" | **por tentativa × condicionado à partida** |

**v4** incorpora `Avaliacao_Plano_Resubmissao_v3_IEEE_Access.md`: parecer favorável à
execução, sem reestruturação nem ampliação da bateria. Ajustes da v4 — nomenclatura
dos instrumentos geométricos (§8), 2 m como limiar **diagnóstico** e não requisito
(§8), distância de encerramento aceita como medida física com re-run condicional
(§5-4a), **tabela de reúso de dados + regressão de E3** (§4), definição operacional
completa da métrica de prioridade com horizonte H (§4), e precisões: papel de ε no
encerramento da precedência, escopo dos ~38 s, cruzamentos efetivos em d = R.

---

## 0. Diagnóstico

Os revisores não contestam a arquitetura — contestam **o que o artigo diz que ela é**
e **a quem credita os ganhos**:

- **Atribuição teórica:** título/abstract/keywords prometem Bellman + RL; a ablação
  E0 (η = 0) mostra que o termo de valor não altera nenhuma ação executada.
- **Atribuição empírica:** o ganho de segurança é creditado à camada afetiva, mas KOa
  mostra que vem do *keepout* no costmap — e o baseline principal é cego ao perigo.

Ambos corrigíveis. **O principal contraste experimental ainda ausente** é isolar o
campo afetivo de um desvio genérico (R2#3) — Eixo 3, e é o risco real do plano. Não é
o único lugar onde pode aparecer resultado novo: as sensibilidades e a verificação do
resíduo também podem produzir achados relevantes.

---

## 1. P0 — Higiene de submissão

O R3 reclamou que o manuscrito contém a carta-resposta após as referências e
placeholders de template.

**Verificado:** o `access.tex` não inclui a carta, e os PDFs locais (limpo e
highlighted) têm 16 páginas sem texto de revisor. **O que isso não prova:** qual slot
de upload causou a junção. A hipótese provável é o PDF de revisão mesclado pelo portal
a partir de `author_response.pdf`/`cover_letter.pdf`, mas é hipótese.

- [ ] **Confirmar no portal** o pacote de revisão da submissão anterior antes de
      atribuir a causa. Só então ajustar os slots.
- [ ] Subir a resposta em *Author's Response Files*; conferir o proof mesclado
      página por página **antes** do submit.
- [x] `\history{}`/`\doi{}` — **feito em 2026-10-16.** Ambos passam a ser chamados
      com argumento **vazio**, e não com os valores do template (o DOI de amostra
      `10.1109/ACCESS.0000.0000000` chegou a ficar no arquivo entre `f7dd1ec` e
      `5325ea3` — era justamente o que o revisor chamou de *apparent placeholder
      DOI*). Verificado no `ieeeaccess.cls`, que o autor colocou no diretório em
      2026-10-16: `\history` tem `\let\@history\@empty` (vazio não imprime nada),
      `\doi` **não** tem default (omitir dá erro) e o rótulo `Digital Object
      Identifier` é impresso **incondicionalmente** (l. 700). Ou seja, `\doi{}`
      deixa o rótulo sozinho na capa, sem número — campo visivelmente não atribuído.
      O `VOLUME 11, 2023` fica: vem de dentro do `.cls`.

      **Correção de atribuição:** eu havia escrito, aqui e na carta, que a string
      "Submitted…; revised…; accepted…" vinha do default da classe. Não vinha — o
      `ieeeaccess.cls` não contém essas palavras, logo ela estava no `\history{...}`
      do próprio fonte submetido. O `docs/artigo/access.tex` só entrou no git em
      `f7dd1ec` (2026-10-14), então **não dá para recuperar** o que a versão
      submetida continha. A carta deixou de afirmar a causa e passou a descrever
      apenas o estado atual.
- [ ] Encurtar o corpo movendo configs secundárias (equivalência, dyn-hazard, ruído)
      para apêndice (R3-m3).

---

## 2. Eixo 1 — Reposicionamento (textual)

Atende R2#1 (via b), R3#1, R3-m1. **Maior retorno por esforço do plano.**

- [ ] **Título:** *"A Two-Layer Deliberative–Reactive Architecture with a
      Threshold-Triggered Attraction–Repulsion Layer for Substation Inspection"*.
      Remover "Autonomous" é cosmético e **não resolve escopo sozinho** — o que
      resolve é a afirmação explícita no resumo e na conclusão de que a avaliação é
      em simulação com percepção e localização idealizadas.
- [ ] **Keywords:** remover `Bellman equation` e `reinforcement learning`.
      **Não** incluir `risk-aware navigation`: detectar perigos e aplicar zonas
      proibidas não é modelar risco, e a palavra-chave convidaria um ataque novo.
      Entram `keep-out zones`, `behavior arbitration`.
- [ ] **Abstract:** reordenar — arquitetura → controlador por limiar → achado do
      keepout → escopo (percepção oráculo) → limites estatísticos.
- [ ] **Contribuições:** hoje "arquitetura" e "controlador" se sobrepõem. Separar por
      **tipo de contribuição**, não por componente: (1) o projeto da arquitetura e seu
      árbitro de precedência; (2) a avaliação comparativa em stack ROS 2/Nav2;
      (3) os resultados de atribuição e sensibilidade. Evitar "stack industrial
      padrão" — usar "stack de navegação ROS 2/Nav2".
- [ ] **Conclusão:** espelhar o abstract.
- [ ] **Varredura de coerência** título ↔ abstract ↔ §I ↔ §VI ↔ apêndice. O R2#1
      avisa que o reposicionamento tem de ser levado "consistently" — é onde esse
      tipo de revisão falha.

---

## 3. Eixo 2 — Atribuição do ganho de segurança (KOF)

Atende R3#2. **Uma linha no runner.**

```
run_block KOF 0.0 false route_hazard stay_alert true false
#            η=0  sa=off            keepout=on  avoid=off
```

**Correção da v1 (crítica §6).** A v1 dizia "resultado esperado: KOF empata com RHM".
Errado em duas frentes:

1. Ausência de diferença significativa não demonstra equivalência. Mas **TOST não é
   obrigação automática** (crítica v2 §3): a margem de ±5 s usada para *tempo* não se
   transfere para clearance ou TTC, e com n=10 o teste pode sair inconclusivo mesmo
   com estimativas próximas. → Apresentar **contrastes, intervalos e limitações**.
   Só afirmar equivalência se for possível especificar antes: em qual medida de
   segurança, qual diferença é operacionalmente desprezível, e qual margem
   corresponde a ela. Se não der para justificar a margem, não alegar equivalência.
2. **KOF não pode empatar com RHM em inspeção**: com `sa=false` não há camada reativa,
   logo não há investigação. Confirmado empiricamente — RHB, que também tem `sa=false`,
   inspeciona 0 anomalias em 10/10 runs. **KOF isola a função de segurança, e só ela.**

- [ ] Rodar KOF, n=10 (~75 min).
- [ ] **Comparar as funções separadamente**, nunca num número agregado:
      segurança (clearance mínima, TTC, tempo abaixo do clearance), completude de
      inspeção, custo de missão.
- [x] **Desacoplamento do keepout — PROVADO ESTATICAMENTE (2026-10-13).** A crítica
      avisou que combinação de flags não prova desacoplamento. Está certo, então fui
      à cadeia de lançamento:
      - `experimento.launch.py:47` passa `enable_anomaly: 'true'` **fixo** → o
        `anomaly_simulator` sobe **sempre**, independente de `enable_stay_alert`.
      - `stay_alert.launch.py:119` entrega `publish_keepout` **só** ao
        `anomaly_simulator`; `bellman_node` e `stay_alert_node` são condicionados a
        `when('stay_alert')` = `enable_stay_alert=='true' and reactive=='stay_alert'`.
      - `_emit_keepout` (`anomaly_simulator:400`) é chamado pelo timer do próprio nó
        (2 Hz) e seus **únicos** gates são: `publish_keepout`, existência de perigo,
        `_hazard_live(h)`, pose do robô dentro de `keepout_project_radius`, e TF
        map→base disponível. **Nenhuma referência a nó ou tópico da camada reativa.**
      - Tópico casa: `anomaly_simulator` publica `/hazard_keepout_cloud`;
        `nav2_params_sim.yaml` tem `hazard_layer` consumindo exatamente esse tópico
        (`marking: True, clearing: False`, camada isolada do raytrace do scan).
        Caminho já comprovado em operação por RHM/KOa (1.71 m vs 0.71 m do RHB).

      → **Em KOF sobem:** `anomaly_simulator` (com keepout), `mission_node`,
      `metrics_node` e o stack Nav2. **Não sobem:** `bellman_node`,
      `stay_alert_node`. É exatamente a "ronda fixa + keepout disparado por detecção,
      sem camada reativa" do R3#2.

      **Consequência a declarar:** `anomaly_simulator` assina `/stay_alert/event`
      (linha ~247) para creditar inspeções. Sem `stay_alert_node`, ninguém publica
      esse tópico → `committed`/`completed` ficam vazios → **KOF inspeciona 0
      anomalias por construção**, como RHB. Reforça o §3: KOF isola a função de
      segurança e **nada** mais.
- [~] **Smoke test empírico** (1 run, label `KOFsmoke` — label distinto de propósito,
      para não contaminar o bloco KOF real de n=10).
      **Confirmado no log de lançamento:** sobem apenas `anomaly_simulator-10`,
      `metrics_node-9` e `mission_node-8` (+ stack Nav2). **`bellman_node` e
      `stay_alert_node` não sobem** — a condição `when('stay_alert')` barra os dois,
      exatamente como a análise estática previa.
      Pendente: confirmar `KEEPOUT_FIRST`, o desvio e a folga medida.
- [ ] Se KOF preservar a segurança: declarar no abstract e na discussão que *o
      benefício de segurança é atribuível ao keepout disparado por detecção, não à
      ponderação afetiva* — a alternativa que o R3 oferece textualmente.
- [ ] Reposicionar o fator ≈2.4× de clearance: passa a ser ganho **do keepout** contra
      uma ronda **cega ao perigo**, com a qualificação na mesma frase.

---

## 4. Eixo 3 — Isolar o campo afetivo (decisivo)

Atende R2#3. **Correção da v1 (crítica §3): são duas perguntas, logo duas configs.**

A v1 alterava simultaneamente disparo, seleção e arbitragem — isso compara dois
supervisores completos, mas não atribui diferença à ponderação por saliência.

| Pergunta | Config | Contraste |
|---|---|---|
| A arquitetura oferece benefício sobre uma heurística simples? (R2#3) | **HEU** | supervisor genérico *detect→select→deviate→return*, mesmo Nav2/MPPI |
| A seleção por saliência produz benefício específico? | **HEU-sel** | idêntico ao método **exceto** o critério de seleção |

Base verificada no código: `anomaly_simulator.py:~508` seleciona anomalia por
saliência (`attr_weights[type] * intensity`); `stay_alert_node.py` dispara em
`phi >= enter_threshold`.

- **HEU:** disparo por alcance (`d < R`), seleção por proximidade, arbitragem simples
  "perigo no alcance → desvia".
- **HEU-sel:** só `selection_mode: nearest`. Disparo, histerese, keepout, metas de
  aproximação, confirmação e retorno à patrulha **idênticos** ao método.

- [ ] Manter explicitamente iguais em ambas: percepção, keepout, metas de aproximação,
      confirmação, retorno à patrulha e **orçamento de ajuste** — salvo o que
      constitui deliberadamente a diferença.
- [ ] Implementar `selection_mode: {saliency, nearest}` (`anomaly_simulator`) e
      `trigger_mode: {phi, range}` (`stay_alert_node`) + plumbing.

**Caveat verificado (crítica v2, cuidado 1).** Pergunta: trocar o alvo selecionado
altera indiretamente a magnitude do campo usada no disparo? Auditado:

- **No disparo, não.** O simulador publica a intensidade de **toda** anomalia no raio
  (loop em `anomaly_simulator:~500-508`), e `AttractionField._att` guarda o **máximo**
  |w·intensidade|. O alvo é o argmax; o campo é o max. Trocar o argmax não muda o max
  → o cruzamento do limiar é idêntico. HEU-sel **é** um contraste de um fator no ponto
  de decisão.
- **Ao longo da missão, sim.** `committed` é marcado no alvo escolhido, e anomalias
  committed são **puladas** no loop (linha ~497), logo deixam de alimentar o campo.
  Escolher um alvo diferente muda quais intensidades são publicadas depois → muda a
  **trajetória temporal de Φ**.

- [ ] Documentar essa consequência. **Não** descrever o contraste como "apenas ordem
      de atendimento": é seleção no ponto de decisão **com** efeito a jusante no campo.

### Cenários definidos no plano de análise (correção da crítica §3)

A v1 rodava `conflict`/`adverse` **só se** houvesse empate no default. Isso faria a
bateria parecer busca posterior por cenário favorável — inaceitável para revisores que
já cobram a fronteira confirmatório × exploratório (R2#4).

- [ ] **Declarar antes de rodar:** método, HEU e HEU-sel nos cenários `default`,
      `conflict` e `adverse`. Rodar todos, reportar todos.
- [ ] **Chamar de "plano de análise definido antes das novas execuções", não de
      "pré-registro"** (crítica v2, fechamento). Sem registro formal em repositório
      de terceiros, "pré-registro" sugere um procedimento que não foi feito. E as
      análises sobre dados antigos (re-scoring da confirmação, recontagem de
      exclusões) **continuam retrospectivas**, mesmo planejadas agora — rotular como
      tal.

### Reúso de dados: a lacuna que faltava declarar (crítica v3 §4)

O plano manda comparar método × HEU × HEU-sel nos três cenários, mas o orçamento só
contabilizava os dois comparadores novos. O método **já tem dados** nos três: E3
(default, n=10), CONF (conflict, n=10), E5 (adverse, n=10). O reúso é legítimo — mas
tem de ser **declarado com a condição de comparabilidade**, não assumido.

| Comparação | Dados do método | Dados novos | Condição de comparabilidade |
|---|---|---|---|
| Método × HEU × HEU-sel, por cenário | **reúso:** E3, CONF, E5 | HEU, HEU-sel (×3) | mesmas definições de cenário, parâmetros comuns, métricas e instrumentos |
| RHM/RHB/KOa/KOb × KOF | **reúso:** RHM, RHB, KOa, KOb | KOF | mesmo `route_hazard`, mesma definição dos instrumentos |
| Sensibilidades | **referência:** E3 | limiar, histerese, marginal | alterações deliberadas documentadas |

- [ ] **Condição que licencia o reúso: os parâmetros novos têm de ser no-op na
      configuração default.** `selection_mode=saliency` + `trigger_mode=phi` precisam
      reproduzir o comportamento atual exatamente. → **Rodar 2 runs de regressão de E3
      com o código novo** e conferir contra o E3 antigo antes de aceitar o reúso de 30
      runs (~225 min economizados). Se divergir, a bateria do método é refeita.
- [ ] Registrar **versão do código** (commit) por grupo de dados. Se forem só
      parâmetros novos, modos alternativos e instrumentação sem efeito comportamental,
      o reúso se justifica.
- [ ] **Se a checagem do resíduo (7c) revelar erro de registro ou de comportamento,
      identificar especificamente quais grupos ficaram incompatíveis.** O objetivo não
      é repetir tudo por rotina — é impedir que diferença entre versões de
      implementação seja confundida com efeito do método.

### Métrica independente para saliência

"Escolher a anomalia mais saliente" não é vantagem por si — é reproduzir a própria
regra. Precisa de critério operacional **independente** da regra de saliência.

- [ ] Definir antes de rodar. Candidato: **tempo até inspecionar o evento de maior
      intensidade verdadeira** e **completude sob orçamento de tempo truncado**.
      Ambos deriváveis do `audit_trail.csv` (que já registra `target_true_x/y` e
      timestamps por episódio).
- [ ] **Justificar a métrica, não só escolhê-la** (crítica v2, cuidado 2). "Maior
      intensidade verdadeira" é candidata, mas sua relação com prioridade operacional
      precisa de argumento — sobretudo **entre modalidades**, já que a saliência
      mistura peso de tipo (thermal 1.0, acoustic 1.2) com intensidade. Se a
      prioridade fosse por tipo, o peso 1.2 do acústico **é** a regra sob teste e não
      poderia ser a métrica que a julga → **comparar dentro da mesma modalidade**.

### Definição operacional a fechar antes de rodar (crítica v3 §5)

Comparar dentro da modalidade evita o problema de escala, mas não basta. Fechar os
cinco itens, por escrito, antes da primeira execução:

- [ ] **como o evento prioritário é identificado** — pela intensidade *verdadeira* do
      cenário, independentemente da decisão do controlador (nunca pelo que ele
      escolheu, senão a métrica vira a própria regra);
- [ ] **desempate** — regra fixa declarada (ex. menor id) para intensidades iguais;
- [ ] **instante inicial da contagem** — início da missão, não início do episódio;
- [ ] **orçamento temporal H** — valor único declarado para todos os grupos;
- [ ] **apresentação dos não inspecionados**, com esta formulação:

> **Tempo limitado ao horizonte H:** utiliza-se o instante da inspeção quando ela
> ocorre até H; caso contrário, atribui-se H ao escore e registra-se separadamente que
> não houve inspeção até o horizonte.

- [ ] Relatar **junto** a proporção de eventos inspecionados até H, para que um evento
      inspecionado no limite não fique indistinguível de um nunca inspecionado. E o H
      imputado **não** é tempo observado de inspeção — não apresentar como tal.

**Risco a aceitar:** HEU pode empatar com o método no default. Minha leitura: rodar.
O R2 pediu; omitir numa chance única é pior; e o R3 elogia nominalmente a franqueza
com resultados negativos. Se empatar no default e divergir em `conflict`/`adverse`, a
justificativa fica *mais precisa* que a atual — mas só se a métrica independente
acima mostrar isso, não por reprodução da regra.

---

## 5. Eixo 4 — Sensibilidades

### 4a. Distância de confirmação — **0 runs novos** (R2#5)

**Achado da auditoria.** `inspect_confirm_dist` (default auto = standoff 2.0 + margin
0.8 + 0.5 = **3.3 m**) é uma **função de pontuação pura**: não realimenta o
comportamento. Rastreado em `anomaly_simulator.py`:

- a supressão de re-atração depende só de `committed` (linha ~497), marcado em
  `investigate_start` (linha ~298);
- a confirmação ocorre em `investigate_end` e escreve apenas em `completed`/`failed`
  (linhas ~309–319);
- `failed` **não** remove de `committed` — só `deferred_hazard` remove (linha ~335).

→ Mudar o critério não muda trajetória nenhuma. **A varredura é re-scoring do
`audit_trail.csv`**, que já registra `robot_dist_m` e `threshold_m` por evento de
inspeção. Economiza ~225 min e é metodologicamente superior: mesmas trajetórias,
só o critério varia.

**Correção da v1 (crítica §5).** A v1 afirmava "se a completude recuperar com
confirmação mais folgada, a degradação é do critério". Não decorre: ampliar a
distância só torna mais fácil declarar inspeção concluída.

- [ ] Re-scorar N1/N2/E3 em {2.8, 3.3, 4.0} m a partir do audit trail. **Rotular como
      análise retrospectiva** sobre dados existentes.
- [ ] **Nomear a variável corretamente.** `robot_dist_m` é calculado **no encerramento
      da investigação** (`anomaly_simulator:~311`), não é o mínimo da aproximação.
      Descrever como *"distância ao alvo verdadeiro no encerramento da investigação"*.

**Correção da v3 (crítica v3 §3 — minha recomendação estava excessiva).** A v3 dizia
que o re-scoring "não dá a qualidade física da aproximação" e recomendava re-rodar
E3/N2. Exagero: distância no encerramento **é** medida física, e permite examinar
quão perto o robô estava ao finalizar a ação, como isso varia com o ruído, e quantos
resultados mudam de classificação ao mover o limiar. Acrescento o argumento que fecha
a questão: **a distância no encerramento é mais pertinente à qualidade da inspeção que
o mínimo da trajetória** — a inspeção é o *dwell* no ponto de parada, e um mínimo
pequeno atingido de passagem não demonstra inspeção adequada.

Fato adicional da auditoria: **reconstruir o mínimo dos dados existentes é
impossível** — `pose_logger.py` não está no pipeline da bateria e não há nenhum
arquivo de trajetória em `results/` (as únicas traj CSV são de junho, bateria antiga).
Então a escolha é binária: aceitar a medida de encerramento, ou instrumentar e
re-rodar.

- [ ] **Decisão: aceitar a medida de encerramento.** Rodar primeiro a análise
      retrospectiva de E3/N1/N2 com a variável disponível. O bloco de ~150 min fica
      **condicional**, acionado só se a análise levantar dúvida que ela não resolva.
- [ ] Conclusão defensável: *a completude é sensível ao critério de confirmação*,
      acompanhada da distribuição das distâncias de encerramento. Nada além disso.

### 4b. Precedência de perigo — **três limiares distintos** (R2#6)

**A crítica §4 está certa, e mais do que supunha.** A auditoria de
`attraction_field.py` mostra que os três limiares são:

| | onde | valor |
|---|---|---|
| elegibilidade por modalidade | `thresholds` (dataclass) | thermal 0.4, acoustic 0.3, **hazard 0.3** |
| ε da precedência (Eq. 7) | `_EPS` | **1e-3 — constante de higiene numérica, não parâmetro de projeto** |
| disparo do FSM (retirada) | `enter_threshold` | 0.45 |

Consequências:

1. **Variar `enter_threshold` não testa a precedência.** O que governa a supressão da
   atração é o **limiar de modalidade do perigo (0.3)**, não ε.
2. Esses limiares são *defaults hardcoded* da dataclass, não estão em
   `bellman_params.yaml` → plumbing maior que a v1 estimou.

**Correção da v2 (crítica v2 §1 — erro meu).** A v2 afirmava que "nos parâmetros
atuais não existe faixa de perigo marginal". **Falso.** A conta 1.5 × 0.3 = 0.45 =
`enter_threshold` vale só **no instante de incorporação** de um evento elegível. O
canal de perigo tem memória e decai (`_haz *= 0.85` por segundo), então a faixa
intermediária aparece naturalmente **após a perda de observação**:

| t após perder de vista | `_haz` | domina o campo (> ε=1e-3) | atinge o limiar nominal de entrada (≥ 0.45) |
|---|---|---|---|
| 0 s | 0.450 | sim | sim |
| 1 s | 0.383 | **sim** | **não** |
| 10 s | 0.089 | sim | não |
| ~38 s | <0.001 | não | não |

→ A faixa que o R2#6 questiona existe **sem mexer em limiar nenhum**.

*Escopo do número:* os ~38 s são **calculados para este exemplo** — h inicial 0.45,
decaimento 0.85 por período de 1 s, sem renovação nem reinicialização. Não é duração
universal de supressão: qualquer nova observação do perigo reinicia o canal.

*Papel de ε (precisão da crítica v3 §6):* ε está implementado como tolerância
numérica (`_EPS = 1e-3`), mas **não é só isso** — é ele que determina quando a memória
do perigo deixa de dominar o campo. A divisão certa: o **limiar de modalidade** governa
a *entrada* de novos eventos; **ε governa o encerramento da precedência durante o
decaimento**. A v2 errou ao descartá-lo como mera higiene de float.

A v2 também era forte demais ao dizer "já dispara a retirada no mesmo instante": a
transição depende de `retreat_pose is not None`, do refratário `_avoid_until` e de
`enable_reactive_avoid` (todos em `stay_alert_node._update`). Redação a usar:

> Nos parâmetros atuais, um perigo recém-incorporado na intensidade mínima elegível
> atinge o limiar nominal de retirada. A ocorrência efetiva da transição depende das
> condições do FSM; após decaimento, o canal de perigo pode permanecer dominante
> abaixo desse limiar.

E o resultado a investigar é **supressão da investigação sem disparo de nova
retirada** — não imobilidade. O robô segue a patrulha normalmente; é isso que torna o
modo de falha difícil de notar em operação.

- [ ] Plumbar limiares de modalidade e o par `enter/exit_threshold`.
- [ ] Varrer **limiar de modalidade do perigo** {0.20, 0.30, 0.40} (precedência),
      n=10 → ~225 min.
- [ ] Cenário `conflict_marginal`: perigo logo acima da elegibilidade + anomalia de
      saliência alta, n=10 → ~75 min. **Incluir perda de observação e decaimento no
      próprio ensaio** (crítica v2 §1): o perigo é observado, sai do alcance, e a
      anomalia saliente permanece. É aí que a faixa intermediária age — e não exige
      bateria extra, só o roteiro certo do cenário.
- [ ] **Registrar separadamente** (crítica §4): quando o perigo passa a dominar o
      campo; quando a inspeção é suprimida; quando ocorre retirada; e o custo em
      inspeções, atraso e distância ao perigo. São eventos distintos e hoje o
      instrumento não os separa.

### 4c. Histerese — pares explícitos (R3#3)

Variar `enter_threshold` com `exit_threshold` fixo confunde efeito de limiar com
efeito de largura de histerese.

**Correção da v2 (crítica v2 §4).** O par (0.55, 0.25) da v2 mudava entrada **e**
largura ao mesmo tempo (0.20 → 0.30), justamente o defeito que eu dizia estar
corrigindo. Os três pares certos, sem acrescentar configuração:

| Condição | Entrada | Saída | Largura |
|---|---:|---:|---:|
| Referência | 0.45 | 0.25 | 0.20 |
| Faixa estreita, entrada fixa | 0.45 | 0.35 | **0.10** |
| Faixa deslocada, largura fixa | **0.55** | **0.35** | 0.20 |

- [ ] Rodar esses três. Não é fatorial completo, mas separa **posição da faixa** de
      **largura da faixa**, que é o que torna o contraste interpretável.

---

## 6. Eixo 5 — Consolidar a comparação com APF (R3#3)

**Correção da v1 (crítica §6).** A v1 propunha uma tabela única com RHM/KOF ao lado de
E3/APF/HEU — **cenários diferentes** (`route_hazard` × `default`), o que seria uma
comparação inválida apresentada como direta.

- [ ] **Painéis separados por cenário.** Painel `default`: E3 × APF × HEU × HEU-sel.
      Painel `route_hazard`: RHM × RHB × KOa × KOb × KOF. Nenhuma linha cruzando.
- [ ] Em cada painel: mission time, distância, clearance mínima, inspeções, todos com
      intervalo de confiança.
- [ ] Declarar o **procedimento e o esforço de ajuste do APF** e se foi equivalente ao
      dos limiares do método. O R3 pergunta isso diretamente — é questão de fairness,
      não de números.
- [ ] Números no abstract onde hoje há adjetivo ("more efficiently").

---

## 7. Eixo 6 — Bellman: rebaixar, sem compensar

**Mudança maior da v2.** A v1 queria rebaixar *e* reforçar. Os dois reforços caíram.

### 7a. O lema está retirado (crítica §2 — erro meu)

A v1 propunha limite `ηΦ_max/(1−γ)`. **Errado:** na atualização do manuscrito o termo
ηΦ está **fora** da multiplicação por α —

$$Q \leftarrow Q + \alpha[r + \gamma \max Q' - Q] + \eta\Phi$$

— e o ponto fixo de um estado com auto-laço é

$$0 = -\alpha(1-\gamma)Q + \eta\Phi \;\Longrightarrow\; Q^\* = \frac{\eta\Phi}{\alpha(1-\gamma)},$$

ou seja, o limite da v1 **omitia o fator 1/α**. Coerente, aliás, com a equivalência já
demonstrada no próprio artigo (recompensa aumentada por ηΦ/α).

Também não se pode afirmar que o efeito "se anula com o tempo" só porque há
decaimento: novos eventos renovam o campo, e pares (s,a) que deixam de ser
atualizados **conservam** a perturbação anterior na tabela. E perturbação limitada ou
decrescente existe em outras formas de aumento de recompensa — a propriedade, sozinha,
não demonstra originalidade.

- [ ] **Nada de lema.** O R2#2 oferece explicitamente "or explicitly demote the update
      to a design note" — rebaixar é suficiente e é o que faremos.
**O ponto fixo descritivo também sai** (crítica v2 §5 — aceito). A expressão
$Q^\* = [r + \eta\Phi/\alpha]/(1-\gamma)$ pressupõe o caso simplificado de um estado
com auto-laço, r e Φ constantes; o $20 + 100\Phi$ ainda pressupõe r=1. Não autoriza
dizer que a tabela real seja "um acumulador de Φ reescalado". Serviu para achar o erro
do lema e nada além disso.

E a explicação que eu tentava construir com ele já existe, mais precisa e sem
matemática nenhuma:

> As diferenças em Q não explicam a ausência de diferenças comportamentais. A
> explicação é estrutural: **Q não seleciona as ações executadas.**

- [ ] Usar essa frase. Rebaixamento limpo, sem compensação.

### 7b. QD/QD0 saem do artigo (crítica §1 — aceito)

`qdriven_node.py` e `train_qdriven.py` já existem (Q seleciona a ação executada,
mapeia para `/cmd_vel`, ε-greedy no treino, greedy na execução) e nunca foram rodados.
A v1 os punha no apêndice.

Aceito a objeção: pôr no apêndice **não reduz a obrigação de validar**. Uma política
que de fato controla o robô reabre treinamento, convergência, transferência do sim
cinemático para o Gazebo, sementes e intervenção do filtro de segurança — e 10 runs de
uma única política treinada não avaliam variabilidade de aprendizado. Os revisores
ofereceram a alternativa de reposicionar; **não é preciso cumprir as duas**.

- [ ] **Fora desta resubmissão.** Fica para um trabalho próprio, onde o treinamento
      possa ser avaliado com o rigor que exige.
- [ ] Nota: o filtro por `/scan` (`safety_dist`, `safe_cone`) não é "muleta" — é
      componente cuja intervenção precisa ser **declarada e medida** quando essa
      investigação for feita. (Retiro o termo da v1.)

### 7c. Esclarecimentos que ficam

- [ ] **Circularidade do |Φ| no estado** (R2#10). Explicar a ordem de cálculo ajuda,
      mas é insuficiente — e a auditoria dá o motivo concreto: `discretize(x, y,
      abs(phi))` usa o **módulo**, então *atração e repulsão de mesma magnitude caem
      no mesmo estado*. O estado também não carrega memória nem configuração dos
      eventos, e o bucket satura (clip de |Φ| é 2.0, o bucket clampa em 1.0). Dizer
      isso explicitamente, com notação temporal/observacional precisa. Reforça o
      rebaixamento em vez de contradizê-lo.
- [ ] **Descontinuidade em d = R** (R2#8). Uma contagem global de transições **não**
      identifica efeito da fronteira (crítica §7). Relacionar cruzamentos da fronteira,
      sinal observado e transições do FSM, em **ensaio dirigido**.
      **Correção (crítica v3 §6):** a v3 dizia "trajetória tangente" — errado, uma
      tangente pode só **tocar** a fronteira e não exercitar a descontinuidade.
      O ensaio precisa garantir **cruzamentos efetivos nos dois sentidos**, de dentro
      para fora e de fora para dentro, com repetição.
- [x] **Fig. 7 / resíduo — CHECAGEM FEITA (2026-10-13): instrumento sem defeito,
      nenhum resultado precisa ser recalculado.** O item bloqueante está liberado.

  **O que gerou a dúvida (v2/v3):** `update_residual = α·q_convergence` exato nos
  valores **finais** de todos os runs e todos os η. **Explicação confirmada: efeito da
  janela final.** No fim da missão o robô está de volta à patrulha e o campo decaiu,
  logo Φ=0 e o resíduo completo degenera em α·|δ| para qualquer η.

  **Teste 1 — aritmética do update** (`scratchpad/test_qtable.py`, Python puro):
  `Q_depois − Q_antes == α·δ + η·Φ` exato (erro < 1e-12) para η ∈ {0, 0.5, 0.8} e
  Φ ∈ {0, ±0.8, ±1.2, 2.0}. `mean_abs_full` reflete o termo afetivo sempre que η≠0
  **e** Φ≠0. Ordem de leitura do código está correta (`full` antes de `td`, que reseta
  ambas as janelas).

  **Teste 2 — série temporal completa** (378 amostras/run, não só o valor final):

  | cfg | η | amostras com \|full\| ≠ α·\|td\| | máx \|full − α·td\| |
  |---|---|---|---|
  | E0 | 0.0 | **1 / 3754 (0.0%)** — e é ruído de float (5.6e-17) | 5.6e-17 |
  | E2 | 0.3 | 2407 / 3756 (64.1%) | 0.209 |
  | E3 | 0.5 | 2379 / 3768 (63.1%) | 0.350 |
  | E4 | 0.8 | 2400 / 3762 (63.8%) | 0.558 |

  O termo ηΦ **está registrado**, em ~64% das amostras, com magnitude escalando
  proporcionalmente a η. Exatamente o comportamento esperado da Eq. (8).

  **Semântica da coluna, para a legenda:** `update_residual` é a **média de
  \|α·δ + η·Φ\| sobre a janela de 1 s** — magnitude, agregada, **não** instantânea e
  **não** assinada. `q_convergence` é a média de \|δ\| na mesma janela. A legenda tem
  de dizer isso: a figura não pode mostrar sinal nem dinâmica instantânea.

  **Detalhe de proveniência (não é bug):** o Φ usado no update é lido no callback de
  odometria (`bellman_node:99`); o Φ publicado em `/stay_alert/attraction` é lido no
  timer de 1 Hz (`_tick`). Mesmo objeto `AttractionField`, instantes de amostragem
  diferentes. Vale uma frase na descrição de proveniência.

- [ ] **Oportunidade de custo zero descoberta na checagem: sobrepor η na Fig. 7.**
      Hoje `gerar_qconv.py` plota **só o E3** — então a única figura dedicada ao update
      não permite ao leitor ver se η importa. Os dados dos quatro η já existem.
      Medido:

  | | η=0 (E0) | η=0.3 | η=0.5 | η=0.8 |
  |---|---|---|---|---|
  | pico da média do resíduo | 0.0965 | 0.1894 | 0.2633 | 0.3712 |
  | AUC (mediana por run) | 0.0802 | 0.0877 | 0.0937 | 0.1066 |

      **Separação completa**: U = 100/100 para E0 contra cada η>0 (todo run de E0 tem
      AUC menor que todo run dos demais; Cliff's δ = 1.0).

      - [ ] Regerar a figura com as quatro curvas sobrepostas.
      - [ ] **Enquadrar com precisão, sem inflar:** o resíduo contém ηΦ por definição,
            então crescer com η é quase tautológico. O que a figura demonstra é que
            **o update está implementado como especificado e é empiricamente estável**,
            e nada sobre comportamento. Par de afirmações a usar no apêndice:
            *o termo de valor é afetado por η de forma monótona e mensurável; o
            comportamento executado não é — porque Q não seleciona as ações.*
      - [ ] Caveat a declarar: em t normalizado ≈ 0.14 a ordem por η se inverte
            (E2 = 0.014 < E4 = 0.071 < E0 = 0.080), artefato do alinhamento de
            transientes de partida entre runs. Não construir nada sobre essa região.
- [ ] A figura vai para o apêndice pelo reposicionamento editorial, independentemente
      do resultado desta checagem.

---

## 8. Eixo 7 — Estatística e contagens

**Contagens verificadas** (160 tentadas, 154 válidas, 6 excluídas — bate com o artigo):

| cfg | válidas | bound 95% (0 contatos) |
|---|---|---|
| CONF, DHb, E0–E5, KOa, N1, RHB | 10 | **25.9%** |
| APF, KOb, N2, RHM | 9 | **28.3%** |
| DHa | 8 | **31.2%** |

- [ ] **Usar o denominador correto** (crítica §7). O artigo cita ~26%, que só vale
      para os grupos de n=10. DHa (n=8) dá **31.2%** — materialmente pior.
      Verificado: `collisions = 0` em **todas** as 16 configurações, então o bound se
      aplica a todas (crítica v2 §2 pedia conferir isso).
- [ ] **Bound junto às alegações** (R2#4), na mesma frase do abstract e da conclusão
      que afirma ausência de contatos, não num parágrafo de ameaças à validade.

### Os dois instrumentos de segurança (achado da 2ª auditoria)

São raios diferentes, e a distinção não está clara no abstract:

| métrica | raio | o que mede |
|---|---|---|
| `collisions` ("contact region") | **0.5 m** | **entrada numa região definida operacionalmente** — 0 em tudo |
| `safety_zone_violations` | **2.0 m** | entrada no **limiar diagnóstico** de folga |

**Nomenclatura (crítica v3 §2).** O comentário do código diz "contato efetivo", mas o
instrumento é `d_now < collision_radius` — **entrada numa região geométrica, não
contato físico**. "Colisão física detectada" exigiria contatos do simulador ou
geometria de colisão. Verificado que **o manuscrito já acerta nisso** (§IV: "a
simulated proxy rather than a physical contact sensor"; §V: "counts entries into a
simulated contact region… not readings of a physical contact sensor"). O erro de nome
era do meu plano, não do artigo — corrigido acima.

**Instrumentos auditados (2026-10-13), `metrics_node`:**

- posição do perigo = **verdade de terreno** (`scenario_events(scenario)[1]`, usa
  `h['x'], h['y']` direto), não a percebida. Confere com o §IV do artigo ("computed
  from the true hazard position"). Assimetria correta: **o sistema age pela percepção,
  a medição usa a verdade**.
- pose do robô via **TF map→base_footprint**, não `/odom` (que está deslocado do
  spawn). Distância percorrida essa sim usa `/odom`, por ser relativa.
- `d_now` = **mínimo sobre todos os perigos** (relevante no `adverse`, com 2 eventos).
- ambos os contadores são **disparados por borda** (`_in_collision`, `_in_clearance`):
  contam **entradas**, não ticks. Logo `safety_zone_violations = 1` por run significa
  um episódio de entrada, não um tick isolado.
- `collision_radius=0.5` e `clearance_threshold=2.0` são defaults do nó e **não são
  sobrescritos** em `bellman_params.yaml` (cuja seção `metrics_node` só traz
  `output_dir` e `run_label`) → são os valores usados na bateria. Confirmado.
- **Calibração para o leitor:** `robot_radius = 0.25` m no Nav2. Como as distâncias
  são centro-a-centro, a "região de contato" de 0.5 m corresponde ao corpo do robô a
  **0.25 m** do centro do perigo, e o limiar de 2.0 m a **1.75 m** da borda do robô.
  Vale dizer no texto — sem isso o leitor não consegue calibrar o que 0.5 m significa.
- **Ressalva já declarada no artigo** (§V, "whole-mission"): em `dyn_hazard` o
  `metrics_node` mede a distância ao perigo desde t=0, **inclusive antes da
  ativação**, porque a lista de perigos é estática. Não afetou os resultados (DHa
  2.55 m, DHb 2.22 m, ambos > 2.0 → 0 violações), mas é bom que siga declarado.

**Escopo dos bounds.** 25.9/28.3/31.2% são a probabilidade **por execução do evento
operacionalmente contado**, nas condições estudadas. **Não** são limite geral para
falha de segurança, colisão física ou operação em subestação real. Dizer isso onde o
bound aparecer.

**Os 2 m são diagnóstico, não requisito.** Verificado: o manuscrito os descreve apenas
como "time below a clearance threshold" (§IV) — nunca como requisito do estudo nem como
distância regulamentar. Logo **1.71 m não é descumprimento de requisito**; é incursão
abaixo de um limiar adotado para medir exposição. Não apresentar nenhum dos dois raios
como distância regulamentar de segurança elétrica.

Redação a usar na discussão (crítica v3 §2):

> No cenário com perigo na rota, o sistema completo aumentou a distância mínima de
> aproximadamente 0,71 m para 1,71 m. Ainda ocorreram incursões abaixo do limiar de
> 2,0 m adotado na avaliação, embora não tenham sido registradas entradas na região
> de contato definida por raio de 0,5 m.

No cenário `route_hazard` a folga mínima do **método completo é 1.71 m** — ou seja,
*dentro* da própria zona de 2 m declarada pelo artigo, com 9.2 s abaixo dela, em
**todos** os runs (RHM 9/9, KOa 10/10; RHB 10/10 a 0.71 m).

**Verificado que o manuscrito já reporta isso corretamente**: Tab. da §V-D traz "Time
below clearance 14.4 vs 9.2 s", e a Tab. de ablação traz KOb a 4.29 m com a ressalva
certa (KOb oscila 29.6×, inspeciona 0.2±0.4 e estoura o tempo em 627 s — a folga alta
é consequência de não vencer o perigo, não conquista de segurança). **Não há defeito
aqui** — fui verificar suspeitando de algo grave e o artigo está honesto.

O que falta é só de apresentação, e é barato:

- [ ] O abstract diz "raises the minimum clearance by a factor of ≈2.4" e "no
      contact-region entries were observed in any scenario" sem dizer que os 1.71 m
      resultantes **seguem dentro da faixa de 2 m**. Dizer na mesma frase. Preempte
      exatamente a crítica que o R2#4 já fez em termos gerais, e o resultado fica
      mais interessante: o ganho é de **margem dentro da faixa**, não de evitá-la.

### Exclusões (crítica v2 §2 — minha afirmação era forte demais)

As 6 exclusões são todas runs de 0 anomalias, logo excluí-las **eleva** a completude
(RHM e APF ambos 2.7 → 3.0; N2 2.1 → 2.33). A v2 dizia "não enviesa RHM × APF".
**Isso mostra apenas que a diferença entre as médias de inspeção não muda nesse resumo
específico** — não demonstra ausência de viés em tempo, distância ou segurança.
Redação a usar:

> A inclusão das falhas de partida não altera a diferença observada entre as médias
> de inspeção de RHM e APF, mas modifica as estimativas absolutas de completude. Não
> se pressupõe independência entre falha de inicialização e configuração.

- [ ] Reportar as duas leituras **explicitamente separadas**:
      **(a) desempenho por tentativa de missão** (incluindo falhas de partida) e
      **(b) desempenho condicionado à inicialização bem-sucedida**.
- [ ] **Para segurança, excluir as runs mortas.** Um run em que o robô não se moveu
      tem 0 contatos trivialmente e **não pode aumentar artificialmente a evidência de
      navegação sem contato**. A direção do ajuste é oposta à da completude — e isso
      precisa estar dito, não deduzido pelo leitor.
- [ ] Tabela de tentativas, exclusões e motivos por grupo (E1–E5 perderam 0, DHa
      perdeu 2) — sem pressupor independência. Responde R3-m2 por inteiro.
- [ ] **Unidades do abstract** (R2#7). **A crítica §7 está certa e a v1 estava errada:**
      verificado, E5 = [5,5,5,5,5,4,5,5,5,5] → **9 de 10 runs com inspeção completa**.
      9/10 é taxa de runs, **não** contagem média. O problema real é outro: 4/9 e 9/10
      são taxas com **denominadores diferentes** (N2 tem 9 válidas, E5 tem 10), e
      "inspects all of them" é uma terceira unidade (anomalias, não runs). Reescrever
      as três com unidade e denominador explícitos.
- [ ] **Fronteira confirmatório × exploratório** (R2#4). Marcar, em cada alegação, de
      qual família vem; declaração no início de §V e prefixo visual nas tabelas.
- [ ] **Legenda da Fig. 7** (R2#9): a banda é dispersão inter-run, não IC da média.
      Está no texto; tem de estar **na legenda**.
- [ ] **Generalidade** (R2#5, R3-m1): um cenário denso e dois níveis de ruído não
      sustentam robustez. Qualificar na mesma frase.

---

## 9. Eixo 8 — Trabalhos relacionados (R2-Q3, R3-Q4)

Hoje **21 referências**. O R3 é específico: risk-aware/safety-filtered navigation e
keep-out/zonas restritas em stacks padrão estão finos "given that the keepout is the
component that carries the safety result" — e com o Eixo 2 creditando o keepout, a
lacuna fica **mais** exposta.

- [ ] Selecionar por **lacuna argumentativa, sem meta numérica** (crítica §7): o que
      falta é síntese crítica, não contagem. Os revisores pedem engajamento com como
      os métodos concorrentes tratam arbitragem, formalização de segurança e incerteza
      de percepção.
- [ ] **Tab. 1: de matriz de features para comparação de premissas** (R2-Q3 é
      textual). Colunas: o que cada método assume sobre percepção; como arbitra
      comportamentos conflitantes; se formaliza segurança; como trata incerteza.
- [ ] **Sondar as limitações, não só declarar** (R2-Q3). Os Eixos 3–4 fazem isso para
      três delas; a §limitações passa a apontar para os experimentos.

---

## 10. Dimensionamento

Blocos medidos no `results/bateria_blocos.log`: **70–90 min por bloco de 10 runs**.

| Bloco | n | Parede |
|---|---|---|
| KOF | 10 | ~75 min |
| HEU × {default, conflict, adverse} | 30 | ~225 min |
| HEU-sel × {default, conflict, adverse} | 30 | ~225 min |
| Limiar de modalidade do perigo {0.20, 0.30, 0.40} | 30 | ~225 min |
| `conflict_marginal` (c/ perda de observação + decaimento) | 10 | ~75 min |
| Histerese: (0.45,0.35) e (0.55,0.35) | 20 | ~150 min |
| Ensaio dirigido d = R (tangente) | 5 | ~40 min |
| Regressão de reúso: 2 runs de E3 com código novo | 2 | ~15 min |
| Confirmação {2.8, 3.3, 4.0} | — | **0 (re-scoring retrospectivo)** |
| Método em default/conflict/adverse | — | **0 (reúso de E3/CONF/E5, se a regressão passar)** |
| *condicional:* re-run E3/N2 c/ distância mínima | 20 | ~150 min |
| ~~QD / QD0~~ | — | **fora** |

**Obrigatório: 1.015 min = 16 h 55 min ≈ 2 noites** no cron das 19h (+15 min da
regressão). Com o bloco condicional de 4a: 19 h 25 min ≈ 3 noites. (Totais conferidos
contra a crítica v3 §6.) Antes de considerar eventuais repetições que a checagem do
resíduo venha a identificar.

A composição melhorou frente à v1 (~16 h de escopo pior): saíram 150 min de QD/QD0 e
225 min da varredura de confirmação; **o reúso de E3/CONF/E5 economiza outros ~225
min** e entraram HEU-sel e os cenários declarados em plano prévio, que é onde o valor
está.

Antes: ~1,5 dia de implementação (dois modos de HEU, plumbing de limiares de
modalidade e do par entrada/saída, cenário marginal, script de re-scoring) **+ a
checagem de instrumentação do resíduo (7c), que é bloqueante**: se houver erro de
registro, ela define quais resultados precisam ser recalculados — e isso muda o resto
do cronograma. Fazer **primeiro**.
Depois: reanálise, figuras, reescrita dos eixos textuais, carta-resposta.

**Ordem de execução** (crítica v3, sequência recomendada):

1. ~~**Verificar a instrumentação do resíduo** (7c)~~ — **FEITO 2026-10-13: passou.**
   Instrumento sem defeito, nenhum resultado afetado, nenhuma repetição necessária.
   Consequência: **o reúso de E3/CONF/E5 não está comprometido por 7c** (resta só a
   regressão de no-op dos parâmetros novos, §4).
2. **Confirmar os instrumentos geométricos de segurança** (0.5 m / 2.0 m) e o
   **funcionamento isolado de KOF** (keepout publica com a camada reativa desligada).
3. **Fechar as definições operacionais por escrito:** métrica de prioridade, desempate,
   instante inicial, horizonte H, censura, contrastes e **reúso de dados** + regressão
   de E3.
4. **Executar a matriz:** noite 1 (KOF, HEU, HEU-sel), noite 2 (limiar de modalidade,
   `conflict_marginal`, histerese, ensaio d = R).
5. **Reavaliação retrospectiva:** confirmação (re-scoring) e exclusões.
6. **Reescrever** manuscrito e carta-resposta a partir dos resultados.

P0 e Eixo 1 (textuais) podem correr em paralelo a partir de (1), já que não dependem
de dado novo.

**Não acrescentar configuração nova nesta etapa.** A prioridade deixou de ser
redesenhar o plano e passou a ser executá-lo com definições estáveis, rastreabilidade
dos dados e conclusões limitadas ao que cada comparação demonstra.

---

## 11. Mapa de cobertura

| Comentário | Ação | Eixo |
|---|---|---|
| R2#1 Bellman sem instanciação | reposicionar (via b); QD fora do artigo | 1, 7b |
| R2#2 Φ ≡ aumento de recompensa | **rebaixar, sem lema** | 7a |
| R2#3 baseline não isola o campo | **HEU** + **HEU-sel** | 3 |
| R2#4 estatística / bound | bounds por denominador; fronteira conf.×expl. | 8 |
| R2#5 ruído / confirmação | re-scoring retrospectivo + medida física (decisão 3) | 5-4a |
| R2#6 precedência | limiar de **modalidade** + decaimento + `conflict_marginal` | 5-4b |
| R2#7 unidades no abstract | três unidades e denominadores explícitos | 8 |
| R2#8 descontinuidade em d=R | ensaio dirigido tangente, não contagem global | 7c |
| R2#9 banda da Fig. 7 | legenda | 8 |
| R2#10 circularidade do \|Φ\| | módulo colapsa atração/repulsão; notação precisa | 7c |
| R2-Q3 related work / Tab. 1 | Tab. 1 de premissas; sondar limitações | 9 |
| R3#1 reposicionar Bellman/RL | título, keywords, abstract, contribuições, conclusão | 2 |
| R3#2 segurança vem do keepout | **KOF** + funções separadas + dois instrumentos | 3, 8 |
| R3#3 APF subdesenvolvido | painéis por cenário + tuning + histerese | 6, 5-4c |
| R3-m1 percepção oráculo | afirmação explícita no abstract e conclusão | 2 |
| R3-m2 contagens por config | n por grupo; manchetes com e sem exclusões | 8 |
| R3-m3 carta no PDF | confirmar no portal; encurtar main text | 1 |
| R3-Q4 refs risk-aware/keepout | por lacuna argumentativa | 9 |
| R1 | nada | — |

---

## 12. Decisões antes de começar

**Resolvidas** (não precisam mais de decisão): lema → fora; QD/QD0 → fora; ponto fixo
descritivo → fora; TOST para KOF → só com margem justificada; distância mínima →
aceitar a medida de encerramento, bloco condicional; cenários → declarados em plano
de análise, com reúso de E3/CONF/E5 sob regressão.

**Nenhuma configuração nova entra nesta etapa.** O que resta é fechar definições.

1. **Rodar HEU + HEU-sel nos três cenários**, aceitando o risco de empate. É o item
   que pode piorar a narrativa. Recomendo sim.
2. **Métrica de prioridade — os cinco itens do §4 (Eixo 3).** Minha proposta fechada,
   para você aprovar ou ajustar: prioridade pela **intensidade verdadeira dentro da
   mesma modalidade**; desempate por **menor id**; contagem desde o **início da
   missão**; **H = 400 s** (acima dos ~372 s do método em `route_hazard` e dos ~365 s
   da missão nominal, abaixo do timeout de 600 s); não inspecionado até H recebe **H
   no escore, reportado separadamente** junto da proporção inspecionada até H.
3. **`\history`/`\doi`:** neutralizar (recomendado).
4. **Título sem "Autonomous"** — mexe no título que o editor já tem em ficha.

O item 2 é o único que trava a execução: os passos 1–3 da ordem acima podem começar
sem ele, o passo 4 não.

