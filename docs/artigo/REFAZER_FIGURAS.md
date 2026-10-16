# Figuras a refazer — resubmissão Access-2026-46291

Auditoria de 2026-10-14, após a reescrita. **Três figuras contradizem o
reposicionamento** e precisam ser re-renderizadas no Illustrae; as demais já foram
corrigidas ou estão corretas.

> **STATUS 2026-10-16 — CONCLUÍDO.** As três voltaram do Illustrae com todas as
> alterações aplicadas (inclusive o rótulo opcional do canal de keepout), foram
> conferidas uma a uma e convertidas para PDF (1200×1200 RGBA → 288×288 pt @ 300 dpi,
> alfa achatada sobre branco). Pendência cosmética única: ver nota no fim do item 2.

## Por que isso importa

O R3#1 pede que título, abstract e keywords não prometam um componente de
aprendizado que o sistema avaliado não tem, e o R2#1 avisa que o reposicionamento
"must be carried through... consistently". Corrigimos o texto — mas **as Figuras 1
e 2 continuam exibindo a equação de Bellman em caixa de destaque**. Um revisor
reabrindo o PDF vê a contradição antes de ler o abstract corrigido.

---

## 1. `concept_overview` (Fig. 1) — REFAZER

**Problema:** caixa inferior "passive value-update substrate (not actuated)" com
`Q ← Q + α[r + γ max Q' − Q] + ηΦ` em destaque, ocupando a largura toda.

**Ação:** **remover a caixa inteira.** A atualização de valor agora é nota de
projeto no Apêndice, não parte do conceito. Nada entra no lugar — a figura ganha ar
e o conceito (ronda ativa + atração/repulsão) fica mais legível.

**Resto da figura:** correto. Manter "active-sensing patrol (Nav2)", "Φ → threshold",
"repel (Φ<0): retreat" e "attract (Φ>0): approach & inspect".

## 2. `architecture` (Fig. 2) — REFAZER

**Problemas:**
- caixa "Bellman value update (passive)" com a equação e a legenda "computed but not
  actuated — substrate for a future learned policy";
- título do bloco inferior: "Reactive affective — Stay Alert".

**Ações:**
- **remover a caixa do Bellman** e a seta tracejada que leva a ela;
- título do bloco inferior → **"Reactive — Stay Alert"**;
- "Affective field Φ" → **"Attraction–repulsion field Φ"**;
- *(opcional, reforça o achado central)* rotular o canal verde do keepout como
  **"keepout channel — carries the clearance result"**.

**Resto:** correto. Manter os blocos deliberativos, o canal `/cmd_vel`, o retorno de
pose/eventos e a FSM.

> **Nota após a entrega (cosmética, opcional).** A caixa do Bellman saiu, mas o painel
> laranja manteve a altura: sobrou uma faixa vazia de ~14% da altura no rodapé. Como a
> figura entra em `\columnwidth`, isso encolhe todo o texto em ~14% sem necessidade.
> Se quiser pedir um ajuste: *"encurtar o painel laranja para eliminar o espaço vazio
> abaixo da FSM, mantendo tudo o mais igual"*. Não bloqueia a submissão.

## 3. `GA.png` (graphical abstract) — REFAZER

**Problemas:**
- "Reactive **affective** layer";
- rodapé: "safe hazard retreat — **zero collisions**, at a modest time cost".

**Ações:**
- "Reactive affective layer" → **"Reactive layer"**;
- rodapé → **"inspects all three anomalies; clearance from the keep-out, not the
  weighting"**. O "zero collisions" sai: é a alegação que o R2#4 diz ser mais forte
  do que a amostra sustenta, e aqui aparece sem o bound, no artefato mais visível.

A legenda textual (`graphical_abstract_caption.txt`) **já foi reescrita** e não tem
mais "affective", "autonomous", "Bellman" nem "zero collisions".

---

## Já resolvidas, sem ação

| figura | situação |
|---|---|
| `stay_alert_fsm` (Fig. 3) | **Correta.** Só FSM e campo Φ; nada de Bellman. |
| `qconv` (resíduo) | **Regerada** com os quatro η sobrepostos; foi para o Apêndice. |
| `box_panel` | **Regerada**: saiu o E0 (contradizia o rebaixamento) e saiu o E5 (misturava `adverse` com `default` no mesmo painel); entraram HEU e HEU-sel. |
| `traj_overlay` | Imagem mantida; **legenda** passou a declarar a proveniência (sessão de pose-logging separada, não a bateria reportada). Ver nota abaixo. |
| `world_map` | Estático, o mundo não mudou. |

### Nota sobre `traj_overlay`

As trajetórias vêm de `figs/traj_E1.csv` e `traj_E3.csv`, capturados em **junho**,
antes das correções P0 das rodadas 2–5. O `pose_logger.py` **não está no pipeline da
bateria**, então não há trajetória contínua nos runs reportados e a figura não pode
ser regerada a partir deles sem instrumentar e re-executar.

Optamos por **declarar a proveniência na legenda** e deixar a figura como ilustração
qualitativa, sem alegação quantitativa. Se preferir eliminar a ressalva, a alternativa
é instrumentar o `pose_logger` no launch e rodar 2 runs (~15 min) — mas isso
introduziria uma figura de versão de código diferente da bateria, trocando um
problema de proveniência por outro. A declaração é a opção mais honesta.
