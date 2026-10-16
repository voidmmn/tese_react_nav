# Response to Reviewers — Access-2026-46291

**Manuscript:** "A Two-Layer Deliberative–Reactive Architecture with an Affective
Attraction–Repulsion Layer for Autonomous Substation Inspection"
→ retitled: **"A Two-Layer Deliberative–Reactive Architecture with a
Threshold-Triggered Attraction–Repulsion Layer for Substation Inspection"**
(Global Change **G1**).

We thank the Associate Editor for the opportunity to resubmit, and the three
reviewers for a review that was both demanding and precise. We are grateful that the
decision allowed a further round: the comments identified a mismatch between the article's framing and the scope of its evidence, and addressing them has produced a more precisely delimited contribution. Two reviewers converged on the same
central point — that the value-update formulation is foregrounded in the title,
abstract and contributions while the authors' own ablation shows it does not
influence any executed action — and both identified two alternatives: instantiate the
term in action selection, or demote it. **We have demoted it, and carried that decision
through the title, keywords, abstract, contributions, method, figures and
conclusion.** We also built the comparison that was missing (R2.3) and, in doing so,
arrived at an attribution that is more specific than the one we previously claimed.

As in the previous round we distinguish three kinds of answer: **(i) implemented** —
a code or experiment change was made; **(ii) repositioned** — the claim was re-scoped
to what the evidence supports; **(iii) acknowledged limitation** — the requested
capability lies outside the declared contribution and is stated as a limitation
rather than claimed. Notation:
**G#** = global change; **R{n}.{k}** = Reviewer n, comment k.

---

## What changed, in one paragraph

The revised manuscript focuses on the evaluated deliberative–reactive architecture.
Across the tested scenarios, replacing saliency-based target selection with
nearest-target selection produced **no statistically detectable difference** in the
reported outcomes, with identical discrete counts in the `default` and `conflict`
scenarios and overlapping distributions in `adverse`; we therefore no longer claim a
demonstrated benefit from that selection criterion. The raw-detection supervisor
behaved differently in the conflict scenario, halving the minimum clearance
(4.84 → 2.23 m). Inspection of the logs indicates that it **retains hazard
precedence** — it preempts the investigation three times per run — while its
triggering logic does not use the field's temporal persistence. Because the
trigger-mode switch changes both the decision signal and its persistence, **the
comparison does not isolate persistence alone**, and we report that limitation
alongside the prolonged suppression observed in the marginal-hazard scenario (one of
four inspections forfeited in 10/10 runs). Separately, the static on-route hazard
experiments support attributing the clearance improvement to detection-triggered
keep-out handling.

---

## Global changes

**G1 — Repositioning (R2.1, R3.1).** Title no longer contains "Affective" or
"Autonomous". Keywords no longer contain "Bellman equation" or "reinforcement
learning"; we deliberately did **not** add "risk-aware navigation", since detecting a
hazard and projecting a forbidden region is not modelling risk and the keyword would
invite a claim we cannot support. The abstract, the contribution list (now three
items organised by *type* of contribution rather than by component), §III-B, the
conceptual figures and the conclusion were rewritten accordingly. The value update
moved to Appendix (Design Note).

**G2 — The isolating baseline (R2.3).** Two configurations were added on the *same*
Nav2/MPPI controller, perception, keep-out, approach poses, confirmation criterion
and return logic: **HEU**, a generic detect–select–deviate–return supervisor driven
by raw detection with nearest-target selection and plain "hazard in range ⇒ deviate"
arbitration; and **HEU-sel**, a one-factor variant differing from the proposed layer
*only* in the selection criterion. Both were run in three scenarios declared before
execution.

**G3 — The fair safety reference (R3.2).** Configuration **KOF**: fixed patrol with
the same detection-triggered keep-out and no reactive layer at all.

**G4 — Cost and sensitivity of the precedence (R2.6).** Configuration **CM**
(marginally eligible hazard with a legitimate high-salience target nearby) and a sweep
of the modality eligibility threshold that governs the precedence, plus a hysteresis
sweep whose three pairs separate band *position* from band *width* (R3.3).

**G5 — Statistical hygiene (R2.4, R3-m2).** The confirmatory family is declared in
advance and Holm-corrected; everything else is labelled exploratory, and two analyses
are additionally labelled *retrospective*. Binomial bounds are reported per group
denominator (25.9 / 28.3 / 31.2%) rather than as a single ≈26%.

**New evaluation.** 13 new configurations, 130 attempted runs; 127 met the movement
criterion and 3 remained immobile (same start-up failure mode as the earlier battery,
verified: travelled distance ≈1.7×10⁻¹⁶). The previously reported battery is reused unchanged for the proposed method. Before
doing so we ran a regression check on the default path: two runs under the new code
reproduced the seven discrete behavioural counts exactly and fell within the published
range on four continuous metrics. This is a check of scope, not a proof that the new
parameters have no effect anywhere; it covers the default configuration and the
outcomes listed, which are the ones the reused data supply.

---

## Reviewer 1

> *"The author has solved reviewers comments well."*

**Response.** We thank Reviewer 1 for the positive assessment and for the earlier
round's comments, which shaped the ablations this version builds on. **Action:** none
required. We note that the changes made for Reviewers 2 and 3 narrow several claims
relative to the version Reviewer 1 assessed; we believe the result is stronger, but we
flag the change in scope explicitly so it is not mistaken for an oversight.

---

## Reviewer 2

### R2.1 — The value update has no experimental instantiation

> *"Either the value term must be connected to action selection in at least one
> configuration … or the framing must be adjusted so that the update appears as a
> secondary theoretical remark … though it must be carried through the title,
> abstract, contributions, and conclusion consistently."*

**Response (repositioned).** We accept the second option. We agree that presenting the
update "as a substrate" did not justify its prominence. We also agree that the
alternative is substantial work — an exploration policy, an action-to-velocity
mapping and a comparison against ordinary tabular Q-learning — and that doing it
partially would be worse than not doing it: ten runs of a single trained policy would
not characterise learning variability. It is therefore deferred to separate work
rather than appended here.

**Action (implemented).** Title, keywords, abstract, contribution list, §III-B
heading and body, both conceptual figures and the conclusion were rewritten. §III-B
now defines only what the system uses — the field and its arbitration. The update,
its relation to reward shaping, the convergence discussion and the residual figure
moved to the Appendix as a Design Note. The explanation given there is structural
rather than empirical: *the value table does not select the executed actions*, so
differences in Q cannot explain differences in behaviour.

### R2.2 — What is the reader to take from the formulation?

> *"…either derive a property that distinguishes Φ from generic reward augmentation,
> such as a boundedness or decay property with a formal consequence, or explicitly
> demote the update to a design note."*

**Response (repositioned).** We take the second option and demote the update to a
design note.

**Action (implemented).** The update is demoted to a Design Note. No new formal claim
is made. We also corrected a statement from the previous version: we had written that
the complete residual was "comparable across η (≈0.02)". That is true only at
*mission end*, where the field has decayed to zero and the term contributes nothing
for any η. Over the mission the residual separates cleanly by η — it differs from
α|δ| in ≈64% of samples for every η>0 and in none for η=0. The new figure overlays
all four η values and the text states both the separation and its near-tautological
character: the residual contains ηΦ by construction.

### R2.3 — The baselines do not isolate the affective weighting

> *"…it leaves the paper without a comparison that isolates the contribution of the
> affective field from that of a generic detect-select-deviate-return heuristic
> running on the same Nav2/MPPI controller."*

**Response (implemented).** This was the most consequential comment and we agree with
it entirely. We built exactly that baseline (G2), plus a one-factor variant, and
declared the scenarios before running.

**Action.** New §V-C. Results, with the confirmatory/exploratory boundary marked and
with care about what the comparison does and does not establish:

- **Confirmatory, `default`:** across all ten runs of each configuration, the proposed
  layer and HEU-sel produced *the same constant value* on every discrete behavioural
  outcome — 3 anomalies inspected, 1 retreat, 4 route deviations, 0 timeouts, 0
  contact-region entries, 0 clearance-band entries. This is a statement about the
  observed outcomes, not a test result. On the continuous metrics the ranges overlap
  and no difference is detected (p_Holm = 1.0000; |δ| ≤ 0.19). HEU differs in
  retreats, investigation time and duration. The clearance difference does not survive
  correction (p_Holm = 0.0511) and is 6 cm; we report it as operationally irrelevant
  rather than as an advantage.
- **Exploratory, `conflict`:** HEU eventually inspects the anomaly co-located with the
  hazard, and the minimum clearance falls from 4.84 to 2.23 m (Cliff's δ = +1.00,
  complete separation; CI [+2.60, +2.63] m; p < 0.0001), with 4 retreats instead of 1,
  +106 s of mission, and the priority inspection delayed ≈105 s. Here too the discrete
  outcomes of HEU-sel and the proposed layer are constant and identical across ten
  runs each.
- **Exploratory, `adverse`:** all three configurations inspect four or five anomalies,
  and here the discrete outcomes are *not* constant: anomalies inspected take values
  {4, 5} and route deviations {8…11} for the proposed layer and {8…12} for HEU-sel.
  The distributions overlap and no difference is detected.

**On what we do and do not claim.** We state that no difference was detected between
the proposed layer and the one-factor selection variant, and in the `default` and
`conflict` scenarios that the observed discrete outcomes were identical. We do **not**
claim statistical equivalence: with ten runs per group, failure to detect a difference
does not establish its absence, and we have not specified equivalence margins for
these metrics as we did for mission time elsewhere in the article. The defensible
reading is that the selection criterion had no detectable effect on these scenarios at
this sample size.

**On attribution.** HEU-sel differs from the proposed layer only in the selection
criterion; HEU differs from HEU-sel only in the trigger mode. The conflict-scenario
effect therefore attaches to the **trigger mode**, and we are careful about what that
switch bundles: it replaces a threshold on the decaying field by instantaneous raw
detection, so it changes the trigger *and* removes the field's temporal persistence
from the decision. It does **not** remove the safety precedence — inspection of the
logs shows HEU preempting the investigation three times per run
(`deferred_hazard`), after which the deferral releases the target and the attraction
re-fires, producing the oscillation and, eventually, the inspection. We therefore
attribute the effect to the loss of temporal persistence in the hazard channel rather
than to the absence of a precedence rule, and we present this as the reading most
consistent with the logs rather than as an isolated factor: separating "trigger
source" from "temporal persistence" would require a further variant that we did not
run. The marginal-hazard configuration (R2.6) provides independent evidence that the
persistence is what produces prolonged suppression.

### R2.4 — Confirmatory/exploratory boundary; the ≈26% bound

> *"…the boundary between confirmatory and exploratory claims is not always easy to
> trace … the abstract and conclusion read as though the absence of contact-region
> entries is a stronger result than the sample size can support."*

**Response (implemented).** Agreed on both counts.

**Action.** §V now opens with an explicit declaration of the confirmatory family and
its extent. The family comprises three contrasts, fixed before the new runs — the
proposed layer against the generic heuristic and against the one-factor selection
variant, both in the `default` scenario, and KOa against KOF on the on-route
hazard — each evaluated on the same five outcomes (anomalies inspected, hazard
retreats, minimum hazard distance, mission duration, investigation time). Holm was
applied across the resulting set of fifteen tests, and the corrected values are the
ones reported as p_Holm in the corresponding table. Everything else is labelled
exploratory *in the sentence that states it*, and two analyses are additionally
labelled retrospective. On the bound: it is now reported per denominator — 25.9% for
n = 10, 28.3% for n = 9, 31.2% for the n = 8 group — and placed in the *same sentence*
as the absence of contacts, in both the abstract and the conclusion. We additionally
disclose something the previous version left implicit: on the on-route hazard the
method transits *within* the 2 m advisory clearance band it reports, for ≈9 s per run.
The clearance gain is a gain of margin inside that band, not avoidance of it.

### R2.5 — Confirmation distance; generality of the abstract

> *"…is the reported degradation a property of the method or of the confirmation
> criterion? A sensitivity analysis over the confirmation distance would help
> disentangle these."*

**Response (implemented, retrospective).** The confirmation criterion is a pure
scoring function: it does not feed back into the controller, because re-attraction
suppression keys on the target being committed at episode *start* and a
non-confirmation does not release it. The same recorded trajectories can therefore be
re-scored under other thresholds without new runs, which is what we did.

**Action.** Re-scoring reproduces the published 4/9 exactly at the original 3.3 m
threshold, which provides an internal consistency check of the re-scoring at that
threshold. It also shows the figure to be strongly criterion-dependent: 2/9 at
2.8 m and **9/9 at 4.0 m**. But that is only half the answer, and we report the other
half: the physical closing distance genuinely degrades, from 2.23 m (median) with
clean perception to 2.87 m under high noise, with a maximum of 3.56 m. Both effects
are present. We state the defensible conclusion — the completeness figure is sensitive
to the criterion *and* the approach quality degrades — rather than claiming the
degradation is an artifact. We note the measured quantity is the distance at episode close, not the minimum over
the approach, which is not instrumented per run. On generality we are explicit rather
than implicit: the noise sweep covers two levels and the dense configuration is a
single scenario, so neither supports a scaling claim. The abstract and the conclusion
now state the completeness figures as rates with their denominators and attach the
scenario they were measured in, and the remaining unmodelled factors — localization
error, event persistence, false positives and negatives, map geometry — are listed in
the Limitations paragraph of the conclusion rather than implied.

### R2.6 — Is the precedence operationally sensible?

> *"A sensitivity analysis around the hazard threshold, or a scenario with a marginal
> hazard and a high-value inspection target, would strengthen the claim…"*

**Response (implemented).** We did both, and the answer has two sides.

**Action.** First, a correction of our own analysis: varying the supervisor's entry
threshold does **not** test the precedence, because what governs suppression is the
*modality eligibility* threshold applied before weighting. Sweeping that threshold
over the three values {0.20, 0.30, 0.40} in the conflict scenario: lowering it to
0.20 produced no detectable difference from the operating value (p = 0.39, clearance
4.85 vs 4.83 m); raising it to 0.40 produced a clearance of 3.78 m (δ = +1.00, CI of
the difference [+0.99, +1.10] m, p < 0.0001), consistent with the hazard being
recognised later and therefore closer. We report these two contrasts and do not
characterise a general response curve from three values.

Second, the marginal scenario (CM). Because the hazard channel decays, the weakest
eligible hazard triggers one retreat at its peak and then keeps *governing* the field
below the retreat threshold for tens of seconds. Measured across ten runs: exactly one retreat fires, and the most salient anomaly in
the scenario is **never** inspected (0/10), so the robot ends every mission with 3 of
4. We define the suppression window as the interval between the first and the last
logged sample in which the hazard channel governs the field (Φ < 0) while its
magnitude is below the retreat threshold; so measured, it lasts 69.5 s (range
67.3–72.4). The window is not pure decay: the hazard is re-observed within it, and the
field magnitude rises again in a median of two samples per run, which is why it
exceeds the duration that decay alone from the initial magnitude would give.
Throughout the window the robot's minimum distance to the hazard is 3.92 m (range
3.86–4.06), and the hazard magnitude is below the threshold that would trigger a
retreat — so the suppression persists under the geometric and detection conditions in
which the layer itself would not act on the hazard. We report this as a cost of the design, alongside the clearance it buys.

### R2.7 — Units in the abstract

> *"These are different units (full-inspection rate versus mean count)…"*

**Response (implemented).** Agreed.

**Action.** The abstract now reports completeness uniformly as the **rate of runs
inspecting all anomalies**, each with its own denominator: 10/10 with clean
perception, 4/9 under high noise, 9/10 under dense clustering. The denominators differ
because the valid-run counts differ, which is now stated in the main text next to the
headline numbers.

### R2.8 — Does the discontinuity at d = R affect the FSM?

**Response (implemented, retrospective).** We separate the mathematical point from
what the recorded data can establish.

The discontinuity at d = R follows directly from Eq. (3): the profile yields Iₑ/2 at
the boundary and zero beyond it. That is a property of the equation and is not in
question.

**Action.** In a retrospective analysis we measured two things in the existing logs:
the size of the step in the logged field at recorded event onsets (median 0.436,
maximum 0.686 in the default scenario, matching the |w·Iₑ/2| the profile predicts),
and the intervals between consecutive FSM transitions (shortest 9.8 s in the default
scenario, 7.0–9.6 s under noise and conflict, 0.2 s in the dense scenario). These
observations characterise the logged response, but they **do not isolate the causal
effect of crossing the sensing boundary**, because geometric crossings were not
recorded synchronously with the field. We therefore do not claim that the step fails
to drive the state machine, nor that the analysis rules out boundary-induced
chattering in general. For the shortest intervals, in the dense scenario, the
inspected logs associate them with consecutive servicing of a cluster or with a goal
abort; we limit the statement to that association.

We also removed from the article an earlier inference that treated silences in the
field record as outward boundary crossings. The channels decay rather than switching
off and the field is written only above the residual ε, so a silence begins after the
field has decayed, not when the robot leaves the sensing radius. In every silence
observed, the last written magnitude was the smallest value the record contains
(10⁻³), with no abrupt drops — consistent with decay rather than with departure.
Reported decay durations are computed for a stated initial magnitude and assume no
renewal; a stronger initial reading, or re-observation of the event, changes them. A
direct test of the boundary would require logging the field continuously together
with the geometric range, which we identify as the appropriate instrument rather than
claim to have used.

### R2.9 — The band in the residual figure

**Response (implemented).** Agreed; readers do interpret such bands as inferential.

**Action.** The caption now states it in bold: the band is the percentile band of the
per-run series, i.e. spread *between runs*, and is **not** a confidence interval of
the mean.

### R2.10 — Circularity of Φ in the state definition

**Response (implemented).** The order of computation resolves the mechanics, but we
agree that alone is a thin answer, so we state what the state consequently *cannot*
represent.

**Action.** The Appendix first states the order that resolves the circularity: at each
step the observations and the channel memories determine Φₜ; Φₜ is then discretised
into the state; and only then is the stored value updated from that state. No
quantity derived from Q re-enters Φ, so the dependence is not a loop. It then notes
that because the bucket uses the **modulus**, an
attraction and a repulsion of equal magnitude map to the same state — the
discretisation discards exactly the sign that carries the safety precedence. The
bucket also saturates (all |Φ| ∈ [0.75, 2] fall in the top bucket), and the state
carries neither the decay memory nor the event configuration. A state so defined cannot distinguish situations that the proposed arbitration rule
treats differently — an attraction and a repulsion of the same magnitude are the same
state — which is a further reason the behaviour is governed by thresholds on Φ rather
than by Q.

### R2 — Additional question 3 (comprehensiveness, related work, limitations)

**Response (implemented).** Agreed on all three sub-points.

**Action.** Table 1 was rebuilt as a critical comparison of **assumptions** — what each
approach presupposes about perception, how it arbitrates a conflict between
simultaneously active behaviours, what status its safety mechanism has, how it
represents uncertainty, and the strongest claim its evidence supports — rather than a
feature matrix. A new §II subsection engages with risk-aware and safety-filtered
navigation and with keep-out handling in standard stacks (see R3-Q4). And three gaps
previously *stated* are now *probed*: the over-conservatism risk (R2.6), the
confirmation-criterion sensitivity (R2.5), and the comparison against a generic
same-controller heuristic (R2.3). The gaps that remain stated are those requiring a
different perception model, and we say which.

---

## Reviewer 3

### R3.1 — Framing versus what the experiments show

> *"Terms such as 'Bellman equation' and 'reinforcement learning' in the keywords and
> abstract currently suggest a learning component that the evaluated system does not
> have."*

**Response (repositioned).** Agreed; see **G1** and R2.1. We additionally audited the
**figures**, which the text changes alone would not have fixed: two conceptual figures
displayed the value-update equation in a highlighted box. Both have been re-rendered: the box is
removed, "Reactive affective" now reads "Reactive", and "Affective field Φ" now reads
"Attraction–repulsion field Φ". The graphical abstract was re-rendered on the same
grounds. We mention this because a
reader reopening the PDF would have seen the equation before reading the corrected
abstract.

### R3.2 — The safety result is attributed to the wrong mechanism

> *"A fairer reference for the safety claim is the fixed patrol plus the same
> detection-triggered keepout, with no reactive layer at all."*

**Response (implemented).** We agree, and we built that configuration rather than
only stating the attribution in the discussion.

**Action.** In the static on-route hazard scenario, KOF reaches a median minimum
clearance of **1.73 m** against **1.71 m** for **KOa** (the keep-out-only ablation,
which retains the reactive inspection layer) — a small observed difference of 2 cm
with no statistically detectable difference (p_Holm = 0.42) — and spends 9.0 s below
the 2 m band against 9.3 s. We do not present this as established equivalence. The
abstract and the conclusion now state that, **in this scenario, the clearance
improvement is attributable to the detection-triggered keep-out rather than to the
reactive weighting**. What the reactive layer adds over KOF here is the inspection
behaviour: 0 of 3 against 3 of 3 (p_Holm = 0.0027), at 31 s of extra mission time. We
present the pair as a decomposition of the on-route result, and do not extend it to
the conflict or marginal-hazard scenarios, which concern other aspects of the
behaviour. We also now state the calibration of the
geometric instruments — both are entries into regions defined by centre-to-centre
distance, with a 0.25 m robot radius, and the 2 m value is a diagnostic threshold
adopted for measuring exposure, not a requirement the study declares and not a
regulatory electrical clearance.

### R3.3 — The potential-field comparison is the least developed

> *"Please consolidate the potential-field comparison into one table … state the
> baseline's gains, tuning procedure and whether its parameters were tuned with the
> same effort … and include the hysteresis and threshold values as a sensitivity
> check."*

**Response (implemented).** Agreed on all three.

**Action.** A single consolidated table now reports mission time, distance, clearance,
inspections and time-to-priority-target with bootstrap intervals. On tuning we give the procedure and the parameters rather than a
characterisation. The APF gains were calibrated so that the baseline triggers within
the same sensing radius as the proposed layer — attraction crossing its threshold at
roughly 4–5 m for waypoints and repulsion at the ~4.7 m passage of the beside-route
hazard — which was the comparability criterion we applied. The resulting values are
k_att = 1.5, k_rep = 4.0, k_obs = 0.6, with trigger and exit thresholds of 0.15 and
0.08 on the force magnitude, and a 12 s post-retreat refractory added against the
oscillation that the potential-field formulation is known to exhibit when a patrol leg
passes inside the trigger region. Its approach parameters differ from ours (1.8 m
standoff and a 30 s investigation budget against 2 m and 40 s). These are reported in
the hyperparameter table together with the proposed layer's. Beyond the trigger-range
calibration we did not run a further search over these values, and the time advantage
should be read with that in mind, and the comparison that *does* isolate the supervisor on a
shared controller is the new heuristic baseline. We also removed a sentence from the
previous version that left a same-controller heuristic as future work; it is now part
of the study. On sensitivity: the three hysteresis pairs separate position from width
— reference (0.45, 0.25), narrower (0.45, 0.35), shifted (0.55, 0.35). Between the two widths evaluated in
the `default` scenario, no difference was detected on any reported outcome (p ≥ 0.60);
shifting the entry point raised the counted route deviations from 4 to 8
(p = 0.0003) and shortened episodes, with inspections unchanged at 3 of 3. We limit
the statement to those two widths and that scenario, and note that the route-deviation
metric is sensitive to the entry threshold's position.

### R3 minor 1 — Perception is abstracted; the title should not imply a validated system

**Response (implemented).** Agreed.

**Action.** "Autonomous" removed from the title. More importantly — since removing a
word is cosmetic — the abstract and the conclusion now carry the qualification
explicitly: perception is abstracted to oracle events, the localization transform is
held fixed, and the results characterise the *decision logic*, not a deployable
system. The conclusion has a dedicated Scope paragraph.

### R3 minor 2 — Per-configuration counts; could the exclusion favour a configuration?

**Response (implemented).** Agreed, and the second part deserves a direct answer
rather than an assumption of independence.

**Action.** Valid counts are given in the main text next to the headline numbers, and every rate
is reported against its own denominator. In the earlier battery, n = 10 for every
configuration except APF, KOb, N2 and RHM (n = 9) and DHa (n = 8). In the new battery
of 13 configurations, n = 10 for every configuration except three, which are named
individually so the three exclusions can be accounted for without inference: the
generic heuristic in `default` (n = 9), the generic heuristic in `conflict` (n = 9),
and the shifted-hysteresis configuration in `default` (n = 9). The proposed layer and
the one-factor selection variant retain n = 10 in all three scenarios, which is why
the identity of discrete outcomes reported in R2.3 is over ten runs per group. On bias: all excluded runs inspected zero anomalies, so removing them **raises the completeness
estimates for the affected groups** — for the most affected pair it
raises the proposed layer and APF by the same amount (2.7 → 3.0 each), leaving the
difference unchanged but making both absolute figures conditional on successful
initialization. For safety the adjustment runs the *other* way: a run in which the
robot never moved trivially records zero contact-region entries, so including such
runs would inflate the evidence for contact-free navigation, and they are excluded
from the safety statistics too. We do not claim start-up failure is independent of
configuration; we state the direction of each adjustment and report both views.

### R3 minor 3 — Response letter and placeholders in the manuscript; length

**Response (implemented).** We regret the inconvenience this caused. On investigation, the appended letter did not originate in the manuscript source — the clean and highlighted PDFs
contain no reviewer text — but in how the files were supplied for the review package.
The remedy is at our end: the response is uploaded
only under *Author's Response Files*, and we verify the merged review proof page by
page before submitting.

On the template fields: the demonstration strings the previous round reported
("Submitted...; revised...; accepted...") came from the class file's own defaults,
because the source did not call `\history` or `\doi` at all. Both are now called with
empty arguments, so no placeholder string — including the specimen DOI — is typeset.
The "VOLUME 11, 2023" running head is set inside `ieeeaccess.cls` and is not under
author control; like the publication dates and the DOI, it is assigned by IEEE
production at publication.

**Action (length).** We report what moved and what did not, since the comment named
three groups. The **equivalence** material — the η sweep and the η = 0 ablation, with
the residual figure — moved to the Appendix, which also follows from the
repositioning. The **dynamic-hazard** configurations stayed in the main text: Reviewer
2 identified that finding (the keep-out resolves the static hazard while the retreat
adds margin only for a hazard emerging mid-investigation) as a useful architectural
observation, and moving it to an appendix would displace the result that distinguishes
the two mechanisms. The **perception-noise** configurations also stayed, because the
confirmation-distance analysis requested in R2.5 is built on them and would lose its
referent. We acknowledge that the new baseline, the precedence-cost section and the
two retrospective analyses add length; we judged the comments requiring them to take
precedence over net shortening, and kept each addition to the question it answers.

### R3 — Additional question 4 (references on risk-aware navigation and keep-out)

> *"The related work … is thin given that the keepout is the component that carries
> the safety result."*

**Response (implemented).** Agreed, and the point sharpens under our own new results:
since §V now attributes the clearance to the keep-out, the gap is more exposed, not
less.

**Action.** A new §II subsection positions our mechanism against three lines and
states what it does and does not provide. Safety filters — control barrier functions
and predictive safety filters — obtain formal guarantees by assuming a model of the
dynamics and of the constraint set. Our precedence rule is a behavioural arbitration
and provides none of those guarantees: it certifies no invariant, and the
marginal-hazard results show it can be over-conservative in a way a filter formulation
would make explicit as a trade-off. Risk-aware planning represents and optimises risk;
we do not, which is why we avoid the term. Closest to our mechanism, standard stacks
already expose keep-out zones as a map layer, usually authored statically; our use is
the same mechanism driven at runtime by detection. We state plainly that the
contribution is not the keep-out but the measurement of how much of the safety outcome
is due to it, and the arbitration rule governing when the reactive layer defers.

---

## Closing

We thank the reviewers for helping us clarify the contribution and strengthen its
experimental assessment. The revised manuscript focuses on the evaluated
architecture, reports the absence of a detectable benefit from changing the
target-selection criterion in the tested scenarios, and documents the differences
associated with the field-based and raw-detection triggering modes. It also reports
the inspection cost observed under a marginal hazard, and attributes the clearance
improvement in the static on-route scenario to detection-triggered keep-out handling.
The scope and limitations of each comparison are stated explicitly, both in the
responses below and in the manuscript. We thank the Editor for the opportunity to
resubmit.
