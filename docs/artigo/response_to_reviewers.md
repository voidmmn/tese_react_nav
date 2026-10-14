# Response to Reviewers — Access-2026-33687

**Manuscript:** "Affective Attraction–Repulsion Value Modulation for Reactive
Inspection Navigation in Electrical Substations"
→ retitled: **"A Two-Layer Deliberative–Reactive Architecture with an Affective
Attraction–Repulsion Layer for Autonomous Substation Inspection"** (see Global
Change **G1**).

We thank the Associate Editor and the four reviewers for an unusually careful and
constructive review. The reviewers converged on one central observation, which we
had disclosed in the submitted version and which we now address structurally: in
the tabular instantiation evaluated, the executed behavior is produced by the
threshold-triggered reactive layer acting on the raw affective field Φ, while the
Bellman-value term ηΦ does **not** influence any executed action. We have realigned
the paper's claims with the mechanism that actually controls the robot, and we have
added the ablations, baselines, safety scenarios, statistics, and literature the
reviewers requested.

In the spirit of an honest response, we distinguish three kinds of answer below:
**(i) implemented** — a code/experiment change was made; **(ii) repositioned** — the
claim was re-scoped to what the evidence supports; and **(iii) limitation assumed**
— a requested capability lies outside the declared contribution and is stated as a
limitation rather than claimed. We do **not** represent every experimental request as
having been executed literally. Notation: **G#** = global change referenced by
several points; **R{n}.{k}** = Reviewer n, comment k.

**Evaluation battery (final).** All results were produced by a single uniform battery
of **16 configurations, 10 attempted runs each (160 attempted)**; **154** met the
movement criterion for behavioral analysis and **6** remained immobile (startup
failures, reported separately as a reliability outcome; 96.25%). Valid $n$ is 8–10
per configuration. Headline results referenced throughout:

- The fixed baseline (E1) inspects **0** off-route anomalies; the method (E3) inspects
  **3/3** in the default scenario, as do the η-sweep and the η=0 ablation (E0, E2, E4).
- Under **dense clustering** (E5) the method inspects **4.9/5** on average, with
  **9/10** runs completing all five; under **high perception noise** (N2) full
  inspection **degrades to 4/9** valid runs (the losses are confirmation rejections,
  not collisions), while under moderate noise (N1) it holds at 3/3.
- The potential-field baseline (APF) inspects 3/3 but is slower and uses a different
  controller, so its comparison is qualified.
- On a hazard **on** the patrol route the method (RHM) contours at a minimum clearance
  of **1.71 m** versus the baseline's **0.71 m** (RHB); a keepout/retreat ablation
  shows the **deliberative keepout** is what resolves the static on-route hazard.
- In a **directed emerging-hazard trial**, the reactive retreat adds **+0.33 m** of
  minimum clearance (whole-mission) over keepout-only, at a time cost and by deferring
  that inspection.
- **No contact-region entries (zero collisions) were observed in any scenario.**

**Reproducibility.** The exact package is the tagged release `v1.0-resubmission`,
commit `8ed48680d1c15fe5ac5e1326499e8b4f0e269bf4`. It contains the 160 per-run CSVs,
the analysis script, a per-episode audit trail (`audit_trail.csv`), a provenance
manifest (`PROVENANCE.md`), and SHA-256 checksums (`CHECKSUMS.sha256`). Because the
tag is mobile across revisions, the manifest fixes the reference snapshot for each
data batch by commit.

---

## Global changes (referenced repeatedly below)

**G1 — Reframing (claims aligned to the demonstrated mechanism)** *[repositioned].*
Title, abstract, and contributions were rewritten. The *validated* contribution is
the two-layer deliberative–reactive architecture with the affective "Stay Alert"
layer. The Bellman-value injection ηΦ is presented as a **formulation / substrate for
future learned policies**, with an explicit statement that, in the tabular
instantiation evaluated here, the immediate behavior is threshold-triggered on the
raw field and the value term does not alter executed actions. We removed every
phrasing implying that the modified update inherits the theoretical guarantees of
standard Q-learning.

**G2 — η=0 ablation and FSM×value separation** *[implemented].* We added a
configuration with the Stay Alert layer enabled and η=0 (E0), and vary η∈{0,0.3,0.5,
0.8}. By construction of the code, η has no path to any executed action: the field
published to the FSM is the raw Φ; the Q-table's greedy action is computed but never
actuated; η enters only the numeric Q-update. The behavioral columns are identical
across η (E0 is equivalent to E3 on mission time by a two one-sided test), while only
the internal Q-values change. We therefore present the η-sweep as a **numerical
analysis of the Q-table**, not as behavioral robustness, and name E0 an
"η=0 (affective-value) ablation" rather than "no-value."

**G3 — Reward de-duplication** *[implemented].* The attraction previously appeared
both in the reward and in the external term ηΦ. Φ now enters **once**, through ηΦ.
Attraction and repulsion are symmetric, and the formulation is directly comparable to
potential-based shaping (R2.2).

**G4 — Baselines and ablations** *[implemented + limitation assumed].* (a) Nav2 +
identical FSM **without** the value term (E0); (b) an **artificial-potential-field**
reactive controller (APF); (c) a keepout/retreat mechanism ablation (RHM/KOa/KOb) that
separates the deliberative keepout from the reactive retreat; (d) the fixed baseline
retained only as reference. *Limitation assumed:* we do **not** add a genuinely
Q-actuated learned controller, nor a heuristic supervisor of equal simplicity using
the **same** controller that would isolate the specific advantage of the affective
weighting; the η=0 ablation isolates the value term (it changes nothing) and APF
supplies a reactive-field reference, but the fully-controlled heuristic comparison is
stated as an open limitation of the demonstrated originality (see R2.5/R4.2).

**G5 — Safety scenarios and the two-timescale response** *[implemented].* We added a
hazard placed **on** a patrol leg. The affective repulsion drives a two-timescale
response: a fast reactive retreat, together with projecting the hazard as a
**persistent keepout into the global costmap on detection**, so the deliberative
planner routes around it; the fixed baseline drives straight through. We further added
(i) a **conflict** scenario in which an anomaly and a hazard are co-located and both
in range, genuinely exercising the field's arbitration, and (ii) a **directed
emerging-hazard trial** (DHa/DHb) in which a co-located hazard activates only once the
robot is already investigating, isolating the reactive retreat's transient value.
Reported outcomes: collisions, time below clearance, minimum radial time-to-collision,
minimum hazard distance, and retreat outcomes.

**G6 — Statistics overhaul** *[implemented].* Comparisons use distribution-free tests
appropriate to the data: Mann–Whitney U (exact for untied samples with n₁+n₂≤20; an
exact two-sided permutation p for fully separated constant arms; the tie-corrected
normal approximation with ties), Cliff's δ effect size, 95% bootstrap confidence
intervals, and Holm correction across a pre-declared confirmatory family of seven
comparisons. Equivalence (the η ablation) uses a two one-sided test (TOST) with a
±5 s margin, applied only where variance is positive. Per-mission success uses
Wilson-score intervals; a zero-failure risk bound is reported as the exact one-sided
binomial, distinct from Wilson. The exploratory emerging-hazard contrasts are reported
uncorrected and kept out of the Holm family.

**G7 — Outcome definitions** *[implemented].* Detection, investigation-initiated
(committed), inspection-completed (reached + commanded dwell + independent pose
confirmation within a stated distance of the *true* target), timeout, navigation
failure, and hazard-deferral are now **separate** outcomes. "Anomalies inspected"
counts only confirmed completions; a timed-out or failed investigation never counts as
an inspection. We name the metric a proxy (confirmed arrival), not a physical
inspection.

**G8 — Continuous detection profile** *[implemented].* The event-intensity profile
tapers continuously toward the detection radius, removing the earlier discontinuity and
any chattering concern; we also removed an unsupported promise of a detection-radius
sweep, keeping only the perception-noise analysis actually reported.

**G9 — Literature and comparison table** *[implemented].* The related-work section was
expanded to 21 references (substation robotics incl. DRL/ant-colony planning, active
perception and informative path planning, safe RL, potential-based shaping, behavior
arbitration, hybrid deliberative–reactive control), with a comparison table along
learning strategy, reactive mechanism, active sensing (partial, honestly qualified),
safety handling, validation, and metrics.

**G10 — Robustness** *[implemented + limitation assumed].* Beyond the dense scenario we
inject Gaussian perception noise on event intensity and position at two levels and
report the degradation of inspection completion and the safety margins. *Limitation
assumed:* generalization to arbitrary maps, localization drift, event persistence and
physical perception is not demonstrated and is stated as future work.

**G11 — Metadata, provenance, and reproducibility** *[implemented].* Template
placeholders (history line, DOI, volume/year) are zeroed to mark the manuscript as a
draft; random seeds (per repetition, recorded in each CSV), initialization rules,
real-time factor, hardware, and the exact commit are reported; the released package
adds the per-episode audit trail, the provenance manifest, and checksums.

---

## Reviewer 1

**R1.1 — Policy-invariance / theoretical strength** *[repositioned].*
*Concern:* convergence is only empirical; do not imply the modified update inherits
Q-learning's properties. *Response:* Per **G1**, we claim no inherited guarantees. We
characterize ηΦ as a bounded, time-decaying additive perturbation and state explicitly
that it is **not** policy-invariant (Φ is a single-state, event- and time-dependent
potential, not a difference of a state potential), framing the tabular case as a design
substrate rather than a convergent learner.

**R1.2 — Statistics on degenerate/constrained metrics** *[implemented].*
Addressed by **G6**. For degenerate arms we report the count difference with Cliff's
δ=±1 and exact/permutation p-values (not Welch); Holm correction is applied across the
confirmatory family; a consolidated per-pair table is provided in the appendix.

**R1.3 — General robustness vs a single adverse scenario** *[implemented +
repositioned].* Addressed by **G10/G5**. Under Gaussian perception noise the method
holds at 3/3 under moderate noise but **degrades to 4/9 full inspections under high
noise** (the losses are confirmation rejections, quantified per episode), while no
contact-region entries are observed and the minimum hazard clearance in fact increases
(4.86 m → 5.29 m). We report this trade-off honestly rather than claiming preserved
completeness, and we state the remaining generality limits.

**R1.4 — Convergence from one run; compare to tabular Q-learning** *[implemented +
repositioned].* Addressed by **G2/G6**. The submitted convergence metric **excluded**
the affective term by construction; we now log the **full residual |α·TD + ηΦ|** and
aggregate it across runs with an inter-run band (the value-stability figure is this
aggregate). We reword the claim to empirical stability of the value increments, not
convergence.

**R1.5 — Literature breadth and comparison table** *[implemented].* Addressed by **G9**.

**R1.6 — Mission-time as a trade-off** *[implemented + repositioned].* With clean data
the baseline (≈320 s) is faster than the method (≈364 s, +14%); we report this honestly
as a bounded, measured time cost for the inspection detours, jointly with inspection
completion and safety clearance, and note the method is nonetheless more time-efficient
than the APF baseline. The abstract's earlier "no significant increase" is corrected.

**R1.7 — Abstract wording** *[repositioned].* The abstract now separates the FSM from
the value modification, qualifies stability as empirical, states completeness
numerically (4/9 high noise, 9/10 dense), and describes safety as observed contacts and
measured margins rather than a general guarantee.

---

## Reviewer 2

**R2.1 — The Bellman contribution is not demonstrated; specify the mechanism**
*[implemented + repositioned].* We answer each sub-point and align the claim (G1/G2).
(a) Q did **not** select executed actions — the greedy action is computed but never
sent to the base; motion comes from Nav2 goals issued by the FSM. (b) No exploration
policy acted on the robot. (c) The discrete actions were never mapped to Nav2/MPPI
commands. (d) Q is updated once per odometry callback (we also corrected the action
inference so pure rotation is no longer logged as "stop"). (e) Removing ηΦ changes **no**
executed action. The reactive layer is presented as the validated contribution and the
value update as a substrate; the η=0 ablation (E0) is added.

**R2.2 — Distinction from reward shaping** *[implemented + repositioned].* Strengthened
by **G3** (Φ enters once). We derive that, for fixed α, the external ηΦ term is
equivalent to augmenting the reward by ηΦ/α, make the comparison to potential-based
shaping explicit, and note where our term departs from a policy-invariant potential.
Novelty is claimed for the architecture, not for the update as a distinct RL operator.

**R2.3 — η not tested meaningfully** *[repositioned].* Addressed by **G2**: the sweep is
a numerical Q-table analysis; the executed behavior is invariant to η.

**R2.4 — Value-stability metric excludes the affective term** *[implemented].*
Full residual |α·TD + ηΦ| aggregated across runs, plus a statement of why tabular-Q
convergence assumptions do not apply to a time-varying, decaying, event-dependent Φ.

**R2.5 — Stronger/fairer baselines** *[implemented + limitation assumed].* Addressed by
**G4**: the η=0 ablation (E0) reproduces the method; APF is a reactive-field reference.
We state as an open limitation that a heuristic supervisor of equal simplicity using
the *same* controller — which would isolate the specific advantage of the affective
weighting — is not included; the APF comparison is qualified as differing in controller
and parameters.

**R2.6 — Safety claim weak; hazard beside the route** *[implemented + repositioned].*
Addressed by **G5**. We add the hazard-on-route scenario with safety outcomes, a
keepout/retreat ablation (the deliberative keepout resolves the static hazard; the
retreat alone oscillates), and a directed emerging-hazard trial showing the retreat's
transient value (+0.33 m clearance) with its cost and deferral. We distinguish logical
precedence, the supervisor's `safe` exit, and arrival at the retreat pose, and read
safety as observed contacts and measured margins under finite samples.

**R2.7 — Statistical rigor** *[implemented + repositioned].* Addressed point-by-point by
**G6**. The immobile runs are startup failures in which the robot never moved (distance
≈0); they are reported as a **mission-reliability outcome (154/160 valid, 6 immobile,
96.25%)** and excluded from behavioral statistics, with the observable immobility
criterion distinguished from a certified infrastructure cause. Raw per-run data and a
per-episode audit trail are public.

**R2.8 — Event/inspection definitions and arbitration** *[implemented].* Addressed by
**G7**. Committed vs completed are separated; failures and timeouts are distinct. The
field's arbitration is formalized as a **hazard-first categorical precedence** (Eq. 4):
a repulsive channel above threshold governs the field regardless of a concurrent
stronger attraction — verified in the conflict scenario, where a hazard co-located with
a *more salient* anomaly still preempts inspection. The two-channel memory (magnitude
max-hold with per-channel decay, residual threshold, internal saturation) is described
to match the implementation.

**R2.9 — Overstated statements** *[repositioned].* "Inspects all anomalies" is qualified
to the default scenario and moderate noise; completeness numbers (9/10 dense, 4/9 high
noise) are stated; "no significant increase in mission time" is replaced by a measured
cost; safety is described as observed contacts and measured clearance, not a general
guarantee.

**R2.10 — Literature too limited; support "to our knowledge"** *[implemented].*
Addressed by **G9**; the originality claim is scoped to integration and analysis, an
open matter of scientific merit we do not overstate.

**R2 minors —** *[implemented].* Eq. (3) discontinuity removed (**G8**); Eq. (4)
selection formalized with explicit tie-break (smallest event identity) and the empty-set
per-channel behavior; Φ notation corrected to an action-independent field with a stated
memory approximation; baseline TD=0 explained (the value node is inactive in the
baseline); reproducibility details and metadata added (**G11**).

---

## Reviewer 3

**R3.1 — Additional benefit of Bellman modulation** *[repositioned].* Addressed by
**G1/G2**: in the tabular instantiation the immediate benefit is delivered by the
reactive layer; the value modulation is a substrate for future learned policies, shown
numerically stable but not the driver of the reported behavior.

**R3.2 — Safety with hazard on the route** *[implemented].* Addressed by **G5**:
hazard-on-route scenario, safety metrics, keepout/retreat ablation, and the directed
emerging-hazard trial.

**R3.3 — "Empirical stability" not "convergence."** *[repositioned].* Agreed;
the figure and wording report empirical stability of the value increments over finite
simulations, with no convergence claim.

---

## Reviewer 4

**R4.1 — Value term (the titled contribution) not tested; add η=0; adjust
title/abstract** *[implemented + repositioned].* Implemented as suggested: the η=0
configuration (E0) reproduces the method's behavior, and the title, abstract, and
contributions present the value update as a design proposal for future learned policies.

**R4.2 — Baseline decided by construction; add a comparable reactive scheme**
*[implemented + limitation assumed].* Addressed by **G4**: an APF controller and a
no-value (η=0) ablation are run on the same events, and the keepout/retreat ablation
decomposes the on-route safety mechanism. As under R2.5, a heuristic supervisor with the
*same* controller isolating the affective weighting's specific advantage is stated as an
open limitation rather than claimed.

**R4.3 — Safety claim vs evidence; adverse scenario never exercises
attraction-vs-repulsion conflict** *[implemented + repositioned].* Addressed by **G5**:
a hazard on a patrol leg, a conflict scenario in which an anomaly and a hazard are
simultaneously in range so Eq. (4)'s arbitration is genuinely exercised, and the
emerging-hazard trial. Safety statements are softened to a consistent maneuver and
measured margins rather than a larger incidental clearance or a general guarantee.

**R4 minors —** *[implemented].* Eq. (3) chattering resolved (**G8**); zero-variance
Welch comparisons replaced by count differences with exact tests (**G6**); Acknowledgment
figure order corrected.

---

## Assumed limitations (stated plainly, not claimed away)

To avoid overpromising, we make these limitations explicit in the manuscript and here:

1. **Originality is that of integration and analysis.** We do not isolate the specific
   advantage of the affective weighting against a heuristic supervisor of equal
   simplicity using the same controller; the APF comparison differs in controller and
   parameters. The sufficiency of this originality is a matter of scientific merit for
   the journal to judge.
2. **Validation is in simulation** with abstracted perception and idealized
   localization; generality to arbitrary maps, localization drift, event persistence,
   and physical perception is future work.
3. **Inspection is a proxy** (confirmed arrival within a stated distance of the true
   target with a commanded dwell), not a certification of orientation, image quality, or
   physical diagnosis.
4. **Safety is reported as observed outcomes** — zero contact-region entries and
   measured clearance/TTC margins under finite samples — not as a general physical
   guarantee; logical precedence is distinguished from a physical guarantee.
5. **The value table does not act.** The affective value modulation is a formulation and
   substrate; behavioral reinforcement learning in which the value drives the executed
   action is future work.

---

## Summary of new/changed files (reproducibility)

- **Code:** reward de-duplication (G3); continuous detection taper (G8);
  committed/completed/failed/timeout/deferred outcomes with independent pose confirmation
  (G7); hazard-first categorical field with two-channel memory (R2.8); environmental
  activation of the dynamic hazard before either channel (G5); per-episode audit logging;
  full-residual logging (R1.4/R2.4); APF baseline, η=0 ablation, keepout/retreat ablation
  (G4); safety and dynamic-hazard scenarios (G5); perception-noise parameters (G10).
- **Data:** 16-configuration battery, 160 attempted runs (154 valid); per-run CSVs, a
  per-episode audit trail (`audit_trail.csv`), a provenance manifest (`PROVENANCE.md`),
  and checksums (`CHECKSUMS.sha256`), all public under tag `v1.0-resubmission`
  (commit `8ed4868`).
- **Manuscript:** retitled; abstract, Sec. II–VI, and appendices revised; new baselines,
  ablations, safety and robustness content, statistics, and a comparison table; claims
  re-scoped to the demonstrated mechanism; metadata zeroed.
