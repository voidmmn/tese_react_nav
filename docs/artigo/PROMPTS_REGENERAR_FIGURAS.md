# Prompts Illustrae.CO — Fig. 1, Fig. 2, Fig. 3 (pós-parecer, 2026-09-10)

Regenerar as três figuras conceituais para casarem com o mecanismo CORRIGIDO
(§6–§13) e o Algoritmo 1 atualizado. As legendas no `.tex` já foram corrigidas.
Cole cada prompt no Illustrae.CO; mantenha o estilo técnico limpo das versões
atuais (dois tons, rótulos legíveis).

═══════════════════════════════════════════════════════════════════════════════
## Fig. 1 — `concept_overview.png/.pdf`   (CRÍTICO — refazer)
═══════════════════════════════════════════════════════════════════════════════

**Por que:** a versão atual põe a equação de Bellman `Q ← Q + α[r + γ maxQ′ − Q] +
ηΦ` na base como se fosse o mecanismo que produz o approach/retreat. Isso está
errado: o comportamento é decidido por um LIMIAR no campo Φ CRU (a FSM); o termo de
Bellman é PASSIVO. A figura precisa tirar o Bellman do caminho causal.

**Prompt:**
> A clean technical concept diagram of a two-layer robot inspection system in an
> electrical substation, isometric illustration style, two-tone palette.
> TOP band: a deliberative "active-sensing patrol (Nav2)" drawn as a dashed
> waypoint loop with small node markers.
> CENTER: an inspection robot on the substation floor. To its LEFT, an electrical
> hazard (arc) with a red glow and a label "repel (Φ<0): retreat"; to its RIGHT, a
> hot equipment anomaly (thermal glow) with a label "attract (Φ>0): approach &
> inspect". The red retreat arrow and the green approach arrow BOTH originate from
> a single small central block labeled "affective saliency field Φ  →  threshold"
> — this block is the control path that produces the behaviour.
> BOTTOM: a clearly SEPARATED, visually de-emphasized dashed grey side-box (smaller,
> off to one corner, connected by a thin dotted line, not by a causal arrow) labeled
> "the field is also cast as a passive additive term ηΦ in a tabular value update —
> a substrate for a future learned policy (NOT in the control path)".
> Do NOT place any Bellman/Q equation in the causal path of the approach/retreat
> behaviour; the equation, if shown at all, must be inside the de-emphasized side-box.

═══════════════════════════════════════════════════════════════════════════════
## Fig. 2 — `architecture.png/.pdf`   (melhoria — adicionar o keepout)
═══════════════════════════════════════════════════════════════════════════════

**Por que:** o núcleo já está certo (threshold no Φ cru → FSM; "Bellman value update
(passive) — computed but not actuated"). Falta só o CANAL DO KEEPOUT (o revisor
pediu) e, opcional, a preempção Investigate→Avoid.

**Prompt:**
> A clean two-layer software architecture block diagram, technical style, two-tone.
> TOP block "Deliberative — Active sensing": a "Waypoint patrol (busy: pause/resume)"
> box feeding "Nav2" (containing "NavfnPlanner" and "MPPI"), whose "/cmd_vel" output
> goes to a "Gazebo / Robot (Environment)" box on the right; the robot returns "pose
> (TF) + events" back to the reactive layer.
> BOTTOM block "Reactive affective — Stay Alert": "Events (modality, intensity,
> position)" → "Affective field Φ" (a bell-shaped low→high field) → "threshold on
> raw Φ" → "Stay Alert FSM" with three states PATROL, INVESTIGATE, AVOID and a
> SAFETY-PREEMPTION arrow from INVESTIGATE to AVOID.
> Two labeled control arrows go UP from the FSM to the deliberative layer:
> "FSM → patrol (busy)" and "FSM → Nav2 (preempt: approach/retreat goal)".
> ADD a THIRD labeled arrow from the reactive layer to Nav2's global costmap:
> "on-route hazard → project temporary keepout into the global costmap (perceived
> position)".
> Below the FSM, a SEPARATE de-emphasized box "Bellman value update (passive):
> Q ← Q + α[r + γ maxQ′ − Q] + ηΦ" with the caption "computed but not actuated —
> substrate for a future learned policy".

═══════════════════════════════════════════════════════════════════════════════
## Fig. 3 — `stay_alert_fsm.png/.pdf`   (refazer — falta a preempção)
═══════════════════════════════════════════════════════════════════════════════

**Por que:** o diagrama de estados atual mostra AVOID alcançável só a partir de
PATROL. Falta a preempção INVESTIGATE→AVOID (um perigo interrompe a investigação),
que é o §7.1 corrigido no código, além dos estados de falha e do refratário.

**Prompt:**
> A finite-state-machine diagram for a reactive robot layer, clean technical style,
> plus a small affective-field inset. THREE states as rounded nodes:
> PATROL ("follow waypoints"), INVESTIGATE ("go to inspection pose + dwell"),
> AVOID ("go to retreat pose").
> Transitions (labeled arrows):
>  • PATROL → INVESTIGATE:  "Φ ≥ θin"
>  • INVESTIGATE → PATROL:  "reached + dwell + confirmed  →  inspected  |  aborted/timeout → failed"
>  • SAFETY PREEMPTION into AVOID from BOTH PATROL and INVESTIGATE, drawn as two red
>    arrows converging on AVOID, labeled "Φ ≤ −θin  (hazard preempts any state)"
>  • AVOID → PATROL:  "Φ > −θout (safe) | retreat pose reached (retreated)",
>    with a small note near this arrow: "refractory before AVOID can re-fire".
> Make the failure/deferred outcomes visually distinct from the successful
> "inspected" outcome (e.g., a small red tag), so a navigation that did not succeed
> is clearly NOT an arrival.
> Keep a circular inset showing the Φ field around the robot: green attraction
> gradient on one side, red repulsion gradient on the other, with a legend
> "Φ signal: + attraction / 0 neutral / − repulsion".

**AJUSTE (render entregue divergiu do prompt — 3 erros a CORRIGIR):**
O PNG atual (`stay_alert_fsm.png`) não seguiu o prompt e contradiz o código/Alg.1.
Regenerar corrigindo EXATAMENTE isto:
1. **Um só limiar.** O render rotulou INVESTIGATE→AVOID como `Φ ≤ −θiα`. NÃO existe
   um segundo limiar: o código usa o MESMO `enter_threshold` para entrar em AVOID
   de qualquer estado. Use `Φ ≤ −θin` tanto em PATROL→AVOID quanto em
   INVESTIGATE→AVOID. Não escreva "θiα".
2. **Seta unidirecional para AVOID.** O render usou seta DUPLA (↔) entre INVESTIGATE
   e AVOID. A transição é de mão única INVESTIGATE→AVOID (perigo preempta a
   investigação, desfecho *deferred*). AVOID **sempre** retorna a PATROL, nunca a
   INVESTIGATE. Desenhe INVESTIGATE→AVOID com uma única ponta, e o retorno só como
   AVOID→PATROL.
3. **Nota do refratário SEM override.** O render escreveu "remains refractory…
   *unless Φ ≤ −θin, in which case AVOID takes priority*". Isso é FALSO: no código o
   refratário é um bloqueio rígido — durante `t_ref` o AVOID fica suprimido
   independentemente de Φ, enquanto o keepout deliberativo contorna o perigo.
   A nota deve dizer apenas: "after leaving AVOID, re-entry is blocked for a
   refractory t_ref while the deliberative keepout contours the hazard" — sem
   qualquer cláusula de "unless / takes priority".

═══════════════════════════════════════════════════════════════════════════════
## Graphical Abstract (`GA.png`) — REFAZER o rodapé (texto falso)
═══════════════════════════════════════════════════════════════════════════════

**Por que:** o banner inferior direito afirma "Stay Alert: all inspected
(3/3 · 5/5 dense) + hazard retreat, at a modest time cost". O "5/5 dense" e o "all"
ficaram FALSOS: com os 140 runs, o cenário denso (E5) é 4.7±0.7 (só 8/10 completas)
e a completude cai sob ruído alto. O resto da figura (as duas colunas 1/2, o mapa,
os ícones) está OK — mudar SÓ o texto dos dois banners de baixo.

**Prompt (só os banners inferiores; manter todo o resto igual):**
> Keep the entire graphical abstract unchanged EXCEPT the two bottom banners.
> LEFT banner (with an ✗ icon): "Baseline patrol: 0 anomalies inspected".
> RIGHT banner (with a ✓ icon), replace its text with:
> "Stay Alert: inspects the anomalies + safe hazard retreat — zero collisions,
> at a modest time cost". Do NOT write "3/3", "5/5", or "all inspected".
