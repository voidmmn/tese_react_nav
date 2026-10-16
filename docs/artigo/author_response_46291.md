**Original Manuscript ID:** Access-2026-46291

**Original Article Title:** "A Two-Layer Deliberative–Reactive Architecture with an
Affective Attraction–Repulsion Layer for Autonomous Substation Inspection"
(revised title: "A Two-Layer Deliberative–Reactive Architecture with a
Threshold-Triggered Attraction–Repulsion Layer for Substation Inspection")

**To:** IEEE Access Editor

**Re:** Response to reviewers

Dear Editor,

Thank you for allowing a resubmission of our manuscript, with an opportunity to
address the reviewers' comments.

We are uploading (a) our point-by-point response to the comments (below) (response to
reviewers, under "Author's Response Files"), (b) an updated manuscript with yellow
highlighting indicating changes (as "Highlighted PDF"), and (c) a clean updated
manuscript without highlights ("Main Manuscript").

Two reviewers converged on the same central point: the value-update formulation is
foregrounded in the title, abstract and contributions, while our own ablation shows
that it does not influence any executed action. Both identified two alternatives —
instantiate the term in action selection, or demote it. **We have demoted it**, and
carried that decision through the title, keywords, abstract, contribution list,
method, figures and conclusion; the formulation now appears only as a design note in
Appendix C (pp. 20–23).

We also built the comparison the review found missing — a generic
detect–select–deviate–return supervisor on the *same* Nav2/MPPI controller, plus a
one-factor variant differing only in target selection — and a fixed patrol carrying
the same detection-triggered keep-out with no reactive layer, which is the fair
reference for the safety claim. Thirteen new configurations were run (130 attempted
runs, 127 valid; Table 3, p. 9). The result is an attribution more specific, and more
limited, than the one we previously claimed: replacing saliency-based selection with
nearest-target selection produced **no statistically detectable difference** in the
reported outcomes; the clearance improvement on a static on-route hazard is
attributable to the detection-triggered keep-out rather than to the reactive
weighting; and the precedence rule carries a measured cost, forfeiting one of four
inspections in 10/10 runs of a marginal-hazard scenario. Where a requested experiment
was not performed, or where a comparison does not isolate the factor it appears to
isolate, we say so explicitly and treat it as an acknowledged limitation rather than
a result.

Throughout, we distinguish three kinds of answer: **(i) implemented** — a manuscript,
code, experiment or analysis change was made; **(ii) repositioned** — the claim was
re-scoped to what the evidence supports; **(iii) acknowledged limitation** — the
requested capability lies outside the declared contribution and is stated as a
limitation rather than claimed.

All code, data, a per-episode audit trail, a provenance manifest and SHA-256
checksums of all 290 run files are public under tag `v2.0-resubmission-46291`.

Best regards,

Milton Miranda Neto et al.

---

**Reviewer#1, Concern # 1:** "The author has solved reviewers comments well."

**Author response:** We thank Reviewer 1 for the positive assessment and for the
earlier round's comments, which shaped the ablations this version builds on. We note
that the changes made for Reviewers 2 and 3 narrow several claims relative to the
version Reviewer 1 assessed; we believe the result is stronger, but we flag the change
in scope explicitly so that it is not mistaken for an oversight.

**Author action:** No action was required by this comment.

---

**Reviewer#2, Concern # 1:** "Either the value term must be connected to action
selection in at least one configuration … or the framing must be adjusted so that the
update appears as a secondary theoretical remark … though it must be carried through
the title, abstract, contributions, and conclusion consistently."

**Author response (repositioned):** We accept the second option. We agree that
presenting the update "as a substrate" did not justify its prominence. We also agree
that the alternative is substantial work — an exploration policy, an
action-to-velocity mapping and a comparison against ordinary tabular Q-learning — and
that doing it partially would be worse than not doing it: ten runs of a single trained
policy would not characterise learning variability. It is therefore deferred to
separate work rather than appended here.

**Author action:** We updated the manuscript by rewriting the title, keywords,
abstract and contribution list (p. 1), the heading and body of Section III-B
(pp. 4–6), both conceptual figures (Figs. 1 and 2, pp. 2 and 4) and the conclusion
(p. 19). Section III-B now defines only what the system uses — the field and its
arbitration. The update, its relation to reward shaping, the convergence discussion
and the residual figure (now Fig. 7, p. 23) moved to Appendix C (pp. 20–23) as a
design note. The explanation given there is structural rather than empirical: the
value table does not select the executed actions, so differences in Q cannot explain
differences in behaviour.

---

**Reviewer#2, Concern # 2:** "…either derive a property that distinguishes Φ from
generic reward augmentation, such as a boundedness or decay property with a formal
consequence, or explicitly demote the update to a design note."

**Author response (repositioned):** We take the second option and demote the update to
a design note. We make no new formal claim.

**Author action:** We updated the manuscript by moving the formulation to Appendix C
(pp. 20–23) as a design note. We also corrected a statement from the previous version:
we had written that the complete residual was "comparable across η (≈0.02)". That is
true only at *mission end*, where the field has decayed to zero and the term
contributes nothing for any η. Over the mission the residual separates cleanly by η —
it differs from α|δ| in ≈64% of samples for every η > 0 and in none for η = 0. Figure 7
(p. 23) now overlays all four η values, and the text states both the separation and
its near-tautological character: the residual contains ηΦ by construction.

---

**Reviewer#2, Concern # 3:** "…it leaves the paper without a comparison that isolates
the contribution of the affective field from that of a generic
detect-select-deviate-return heuristic running on the same Nav2/MPPI controller."

**Author response (implemented):** This was the most consequential comment and we
agree with it entirely. We built exactly that baseline — **HEU**, a generic
detect–select–deviate–return supervisor driven by raw detection with nearest-target
selection — on the same Nav2/MPPI controller, perception, keep-out, approach poses,
confirmation criterion and return logic, plus **HEU-sel**, a one-factor variant
differing from the proposed layer *only* in the target-selection criterion. Both were
run in the three scenarios specified in the analysis plan.

**Author action:** We updated the manuscript by adding Section V-B, *Isolating the
Field from the Act of Deviating* (pp. 11–12), reporting Table 7 (p. 14), with the
primary/exploratory boundary marked at each claim:

- **Primary comparison, `default`:** across all ten runs of each configuration, the
  proposed layer and HEU-sel produced the same constant value on every discrete
  behavioural outcome — 3 anomalies inspected, 1 retreat, 4 route deviations, 0
  timeouts, 0 contact-region entries, 0 clearance-band entries. This is a statement
  about the observed outcomes, not a test result. On the continuous metrics the ranges
  overlap and no difference is detected (p_Holm = 1.0000; |δ| ≤ 0.19). HEU differs in
  retreats, investigation time and duration. The clearance difference does not survive
  correction (p_Holm = 0.0511) and is 6 cm; we report it as operationally irrelevant
  rather than as an advantage.
- **Exploratory, `conflict`:** HEU eventually inspects the anomaly co-located with the
  hazard, and the minimum clearance falls from 4.84 to 2.23 m (Cliff's δ = +1.00,
  complete separation; CI [+2.60, +2.63] m; p < 0.0001), with 4 retreats instead of 1,
  +106 s of mission, and the priority inspection delayed ≈105 s. Here too the discrete
  outcomes of HEU-sel and the proposed layer are constant and identical across ten
  runs each.
- **Exploratory, `adverse`:** all three configurations reached a median of five
  credited inspections. The proposed layer completed all five in 9/10 runs, HEU in
  10/10 and HEU-sel in 8/10, so inspection counts varied within the proposed and
  HEU-sel groups while HEU inspected all five in every run. Route deviations take
  {8…11} for the proposed layer and {8…12} for HEU-sel. The distributions overlap and
  no difference is detected.

*On what we do and do not claim.* We state that no difference was detected between the
proposed layer and the one-factor selection variant, and in the `default` and
`conflict` scenarios that the observed discrete outcomes were identical. We do **not**
claim statistical equivalence: with ten runs per group, failure to detect a difference
does not establish its absence, and we have not specified equivalence margins for
these metrics as we did for mission time elsewhere in the article. The defensible
reading is that the selection criterion had no detectable effect on these scenarios at
this sample size.

*On attribution.* HEU-sel differs from the proposed layer only in the selection
criterion; HEU differs from HEU-sel only in the trigger mode. The conflict-scenario
effect therefore attaches to the **trigger mode**, and we are careful about what that
switch bundles: it replaces a threshold on the decaying field by instantaneous raw
detection, so it changes the trigger *and* removes the field's temporal persistence
from the decision. It does **not** remove the safety precedence — inspection of the
logs shows HEU preempting the investigation three times per run (`deferred_hazard`),
after which the deferral releases the target and the attraction re-fires, producing
the oscillation and, eventually, the inspection. We therefore attribute the effect to
the loss of temporal persistence in the hazard channel rather than to the absence of a
precedence rule, and we present this as the reading most consistent with the logs
rather than as an isolated factor: separating "trigger source" from "temporal
persistence" would require a further variant that we did not run. The marginal-hazard
configuration (Reviewer#2, Concern # 6) provides independent evidence that the
persistence is what produces prolonged suppression.

*On the reference arm.* The proposed layer is **reused** rather than re-run in these
three scenarios: configurations E3, CONF and E5 of the earlier battery serve as the
reference arm (Table 3, p. 9). Before reusing them we ran a regression check on the
**`default`** path only: two runs under the new code reproduced the seven discrete
behavioural counts exactly and fell within the published range on four continuous
metrics. We state the limit plainly: that is empirical evidence for `default`, not for
`conflict` or `adverse`, which are also reused. For those two the reuse rests on two
non-empirical grounds — the code changes touch target selection, trigger mode and the
threshold parameters, all of which are pinned to their previous values in the reused
configurations, and the released checksums identify the artifacts — and we present it
on that basis rather than as a verified identity.

---

**Reviewer#2, Concern # 4:** "…the boundary between confirmatory and exploratory
claims is not always easy to trace … the abstract and conclusion read as though the
absence of contact-region entries is a stronger result than the sample size can
support."

**Author response (implemented):** Agreed on both counts.

**Author action:** We updated the manuscript so that Section V (p. 10) distinguishes
the documented timing of the contrasts from the retrospective selection of outcomes.
The released analysis-plan commit containing the three contrasts — the proposed layer
against the generic heuristic and against the one-factor selection variant, both in
`default`, and KOa against KOF on the on-route hazard — precedes the first archived
result file by about an hour. We limit the chronology claim to that documented
ordering. The five outcomes (anomalies inspected, hazard retreats, minimum hazard
distance, mission duration, investigation time) were selected after the runs; the
fifteen tests are therefore reported as a **primary comparison family with
retrospectively specified outcomes**, not as a confirmatory family. Holm adjustment
addresses multiplicity within this reported family; it does not remove the limitations
of retrospective outcome selection.

We also correct an inconsistency we are grateful to have caught before resubmitting.
The consolidated table (now Table 5, p. 12) still listed the seven comparisons that
formed the confirmatory family of the *previous* submission, so the article declared
one family and tabulated another. Table 5 now contains **all fifteen tests and only
those**, with the per-arm n and the procedure used for each, so the Holm denominator
is visible rather than asserted; the seven earlier comparisons move to Appendix B
(Table 13, p. 21) as a historical table, reported uncorrected. The table is generated
from a CSV that the released analysis script writes, rather than transcribed.
Regenerating it from the data corrected **four** p_Holm values that had been
transcribed incorrectly. These comparisons are new in this revision, so the incorrect
values were never part of the version the reviewers received; the correction is
internal to our own drafts, and we record it here because the generated table is the
mechanism that caught it. The 0.0027 that appeared twice on the KOa vs KOF rows
belongs to neither of them: it is the Holm value of the *proposed layer vs HEU
investigation-time* contrast (0.002679), copied onto the wrong rows.

| contrast / outcome | earlier draft | correct |
|---|---|---|
| KOa vs KOF, anomalies inspected | 0.0027 | 1.6×10⁻⁴ |
| KOa vs KOF, mission duration | 0.0027 | 0.0021 |
| proposed vs HEU, hazard retreats | 0.0034 | 3.0×10⁻⁴ |
| proposed vs HEU, investigation time | 0.0034 | 0.0027 |

The two values we did *not* change — 0.0052 for mission duration against HEU and
0.0511 for the clearance — were already correct. None of the four changes a
conclusion. Table 5 and the text now quote the same four-decimal values, taken from
the same generated file.

Everything else is labelled exploratory *in the sentence that states it*, and two
analyses are additionally labelled retrospective. On the bound: it is now reported per
denominator — 25.9% for n = 10, 28.3% for n = 9, 31.2% for the n = 8 group (Section
V-J, p. 18) — and placed in the *same sentence* as the absence of contacts, in both
the abstract (p. 1) and the conclusion (p. 19). We additionally disclose something the
previous version left implicit: on the on-route hazard the method transits *within*
the 2 m advisory clearance band it reports, for ≈9 s per run. The clearance gain is a
gain of margin inside that band, not avoidance of it.

---

**Reviewer#2, Concern # 5:** "…is the reported degradation a property of the method or
of the confirmation criterion? A sensitivity analysis over the confirmation distance
would help disentangle these."

**Author response (implemented, retrospective):** The confirmation criterion is a pure
scoring function: it does not feed back into the controller. The controller ends an
investigation on navigation success plus the commanded dwell and emits an event; a
separate evaluator node receives that event and only then compares the pose with the
true target position to credit or reject the inspection. No episode is prolonged or
shortened by the threshold, and re-attraction suppression keys on the target being
committed at episode *start*, which a non-confirmation does not release. The same
recorded trajectories can therefore be re-scored under other thresholds without new
runs, which is what we did.

We should note that Algorithm 1 did not say this. In the previous version its
`Investigate` exit condition included "final pose within the confirmation distance",
which describes neither the implementation nor the premise this re-scoring rests on.
The implementation was unchanged — it is the pseudocode that was wrong.

**Author action:** We updated the manuscript so that Algorithm 1 and Section III-C
(pp. 6–7) separate the controller's exit from the evaluator's credit explicitly. The
re-scoring is reported in Section V-I (pp. 17–18): it reproduces the published 4/9
exactly at the original 3.3 m threshold, which provides an internal consistency check,
and shows the figure to be strongly criterion-dependent — 2/9 at 2.8 m and **9/9 at
4.0 m**. That is only half the answer, and we report the other half: the physical
closing distance genuinely degrades, from 2.23 m (median) with clean perception to
2.87 m under high noise, with a maximum of 3.56 m. The audit trail separates the two
groups cleanly: of the 27 committed episodes under high noise, the 21 credited closed
at 1.83–3.30 m and the 6 refused at 3.33–3.56 m, none of them an abort or a timeout.
Both effects are present. We state the defensible conclusion — the completeness figure
is sensitive to the criterion *and* the approach quality degrades — rather than
claiming the degradation is an artifact, and we note that the measured quantity is the
distance at episode close, not the minimum over the approach, which is not
instrumented per run. On generality we are explicit rather than implicit: the noise
sweep covers two levels and the dense configuration is a single scenario, so neither
supports a scaling claim. The abstract (p. 1) and the conclusion (p. 19) now state the
completeness figures as rates with their denominators and attach the scenario they
were measured in, and the remaining unmodelled factors — localization error, event
persistence, false positives and negatives, map geometry — are listed in the
Limitations paragraph of the conclusion rather than implied.

---

**Reviewer#2, Concern # 6:** "A sensitivity analysis around the hazard threshold, or a
scenario with a marginal hazard and a high-value inspection target, would strengthen
the claim…"

**Author response (implemented):** We did both, and the answer has two sides.

**Author action:** We updated the manuscript by adding Section V-F, *The Cost of the
Precedence, and Its Sensitivity* (pp. 15–16).

First, a correction of our own analysis: varying the supervisor's entry threshold does
**not** test the precedence, because what governs suppression is the *modality
eligibility* threshold applied before weighting. Sweeping that threshold over the
three values {0.20, 0.30, 0.40} in the conflict scenario: lowering it to 0.20 produced
no statistically detectable difference from the operating value (p = 0.39, clearance
4.85 vs 4.83 m); raising it to 0.40 produced a clearance of 3.78 m (δ = +1.00, CI of
the difference [+0.99, +1.10] m, p < 0.0001), consistent with the hazard being
recognised later and therefore closer. We report these two contrasts and do not
characterise a general response curve from three values.

Second, the marginal scenario (configuration CM; geometry in Table 12, p. 20). Because
the hazard channel decays, the weakest eligible hazard triggers one retreat at its peak
and then keeps *governing* the field below the retreat threshold for tens of seconds.
Measured across ten runs: exactly one retreat fires, and the most salient anomaly in
the scenario is **never** inspected (0/10), so the robot ends every mission with 3 of 4.
We define the suppression window as the interval between the first and the last logged
sample in which the hazard channel governs the field (Φ < 0) while its magnitude is
below the retreat threshold; so measured, it lasts 69.5 s (range 67.3–72.4). The window
is not pure decay: the hazard is re-observed within it, and the field magnitude rises
again in a median of two samples per run, which is why it exceeds the duration that
decay alone from the initial magnitude would give. Throughout the window the robot's
minimum distance to the hazard is 3.92 m (range 3.86–4.06), and the hazard magnitude is
below the threshold that would trigger a retreat — so the suppression persists under
the geometric and detection conditions in which the layer itself would not act on the
hazard. We report this as a cost of the design, alongside the clearance it buys.

We also make the condition under which that window is measured verifiable rather than
asserted. The hand-off that stops a detected hazard being published to the reactive
layer fires only on entry into `Avoid` **and** only where the deliberative keep-out is
enabled. Both experimental matrices (Table 2, p. 8, and Table 3, p. 9) now carry a
retreat column and a keep-out column, so the reader can see that the keep-out is off in
every off-route configuration — including all six HEU and HEU-sel blocks and the
marginal-hazard scenario. In those configurations no hand-off occurs and re-observation
can renew the hazard channel, which is why the measured suppression window (69.5 s)
exceeds the ≈39 s that decay from the initial magnitude alone would give, and why the
HEU contrasts share that condition with the proposed layer rather than differing in it.

---

**Reviewer#2, Concern # 7:** "These are different units (full-inspection rate versus
mean count)…"

**Author response (implemented):** Agreed.

**Author action:** We updated the abstract (p. 1) so that completeness is reported
uniformly as the **rate of runs inspecting all anomalies**, each with its own
denominator: 10/10 with clean perception, 4/9 under high noise, 9/10 under dense
clustering. The denominators differ because the valid-run counts differ, which is now
stated in the main text next to the headline numbers (Section V-J, p. 18).

---

**Reviewer#2, Concern # 8:** "In Eq. (3) the intensity is 0.5·Iₑ at d = R and zero
beyond, so Φ jumps at the detection boundary; a sentence on whether this causes
chattering near R would help."

**Author response (implemented, retrospective):** We separate the mathematical point
from what the recorded data can establish. The discontinuity at d = R follows directly
from Eq. (2) (p. 5): the profile yields Iₑ/2 at the boundary and zero beyond it. That
is a property of the equation and is not in question. What the logs can and cannot
establish about its behavioural effect is a separate matter, and the previous version
overstated it.

**Author action:** We updated the manuscript by reporting, in Section V-I (p. 18), a
retrospective analysis of two quantities measured in the existing logs: the size of
the step in the logged field at recorded event onsets (median 0.436, maximum 0.686 in
the default scenario, matching the |w·Iₑ/2| the profile predicts), and the intervals
between consecutive FSM transitions (shortest 9.8 s in the default scenario, 7.0–9.6 s
under noise and conflict, 0.2 s in the dense scenario). These observations characterise
the logged response, but they **do not isolate the causal effect of crossing the
sensing boundary**, because geometric crossings were not recorded synchronously with
the field. We therefore do not claim that the step fails to drive the state machine,
nor that the analysis rules out boundary-induced chattering in general. For the
shortest intervals, in the dense scenario, the inspected logs associate them with
consecutive servicing of a cluster or with a goal abort; we limit the statement to that
association.

We also removed from the article an earlier inference that treated silences in the
field record as outward boundary crossings. The channels decay rather than switching
off and the field is written only above the residual ε, so a silence begins after the
field has decayed, not when the robot leaves the sensing radius. In every silence
observed, the last written magnitude was the smallest value the record contains (10⁻³),
with no abrupt drops — consistent with decay rather than with departure. Reported decay
durations are computed for a stated initial magnitude and assume no renewal; a stronger
initial reading, or re-observation of the event, changes them. A direct test of the
boundary would require logging the field continuously together with the geometric
range, which we identify as the appropriate instrument rather than claim to have used.
Sections III-B (pp. 4–6) and V-I (p. 18) now carry the same caution: where they
asserted that the step "does not induce chattering" and that an event at the boundary
"cannot repeatedly re-trigger", they now describe hysteresis and commitment as the
mechanisms intended to prevent retriggering, and report the logged onsets and
inter-transition intervals as associations.

---

**Reviewer#2, Concern # 9:** "The band in the residual figure should state whether it
is a confidence interval of the mean or the spread between runs."

**Author response (implemented):** Agreed; readers do interpret such bands as
inferential.

**Author action:** We updated the caption of Fig. 7 (p. 23) to state it in bold: the
band is the percentile band of the per-run series, i.e. spread *between runs*, and is
**not** a confidence interval of the mean.

---

**Reviewer#2, Concern # 10:** "Φ enters the definition of the state while the state is
used to read Φ; the circularity should be addressed."

**Author response (implemented):** The order of computation resolves the mechanics, but
we agree that alone is a thin answer, so we state what the state consequently *cannot*
represent.

**Author action:** We updated Appendix C (pp. 20–23), which first states the order that
resolves the circularity: at each step the observations and the channel memories
determine Φₜ; Φₜ is then discretised into the state; and only then is the stored value
updated from that state. No quantity derived from Q re-enters Φ, so the dependence is
not a loop. It then notes that because the bucket uses the **modulus**, an attraction
and a repulsion of equal magnitude map to the same state — the discretisation discards
exactly the sign that carries the safety precedence. The bucket also saturates (all
|Φ| ∈ [0.75, 2] fall in the top bucket), and the state carries neither the decay memory
nor the event configuration. A state so defined cannot distinguish situations that the
proposed arbitration rule treats differently, which is a further reason the behaviour is
governed by thresholds on Φₜ rather than by Q.

We also corrected the notation the manuscript used around this point. Section III and
the Appendix described Φ as "a function of the state alone" and of "the current
observations alone", which contradicts the decaying channel memories defined in the same
subsection — and it is precisely their persistence that the marginal-hazard scenario
measures. The field is now written Φₜ, a function of the observations *and* the channel
memories; where the appendix writes Φ(s) it states the abuse of notation explicitly,
since two steps with the same discretised state can carry different Φₜ.

---

**Reviewer#2, Additional question 3 (comprehensiveness, related work, limitations):**
"Table 1 functions as a feature matrix rather than a critical comparison of
assumptions; the related work could be broader; and several acknowledged gaps are
stated rather than probed."

**Author response (implemented):** Agreed on all three sub-points.

**Author action:** We updated the manuscript by rebuilding Table 1 (p. 5) as a critical
comparison of **assumptions** — what each approach presupposes about perception, how it
arbitrates a conflict between simultaneously active behaviours, what status its safety
mechanism has, how it represents uncertainty, and the strongest claim its evidence
supports — rather than a feature matrix. In the same table the classical artificial
potential field and the Dynamic Window Approach are now separate rows, since the latter
searches dynamically reachable velocities restricted to those from which the robot can
still stop, rather than summing forces. A new subsection, Section II-D, *Risk-Aware
Navigation, Safety Filters, and Restricted Zones* (p. 3), engages with risk-aware and
safety-filtered navigation and with keep-out handling in standard stacks. And three gaps
previously *stated* are now *probed*: the over-conservatism risk (Concern # 6), the
confirmation-criterion sensitivity (Concern # 5), and the comparison against a generic
same-controller heuristic (Concern # 3). The gaps that remain stated are those requiring
a different perception model, and we say which.

---

**Reviewer#3, Concern # 1:** "Terms such as 'Bellman equation' and 'reinforcement
learning' in the keywords and abstract currently suggest a learning component that the
evaluated system does not have."

**Author response (repositioned):** Agreed; this is the same repositioning described
under Reviewer#2, Concern # 1. We additionally audited the **figures**, which the text
changes alone would not have fixed: two conceptual figures displayed the value-update
equation in a highlighted box. We mention this because a reader reopening the PDF would
have seen the equation before reading the corrected abstract.

**Author action:** We updated the manuscript by removing "Bellman equation" and
"reinforcement learning" from the keywords and the abstract (p. 1), and we re-rendered
both conceptual figures: the equation box is removed, "Reactive affective" now reads
"Reactive", and "Affective field Φ" now reads "Attraction–repulsion field Φ" (Figs. 1
and 2, pp. 2 and 4). The graphical abstract was re-rendered on the same grounds. The
body text was likewise aligned: the component is now named consistently as the
*reactive layer* and the field as the *attraction–repulsion field*, and the novelty
statement in Section II-F (p. 4) no longer claims a term "formulated in the Bellman
update" but the architecture and the attribution it measures.

---

**Reviewer#3, Concern # 2:** "A fairer reference for the safety claim is the fixed
patrol plus the same detection-triggered keepout, with no reactive layer at all."

**Author response (implemented):** We agree, and we built that configuration rather
than only stating the attribution in the discussion.

**Author action:** We updated the manuscript by adding configuration **KOF** — a fixed
patrol with the same detection-triggered keep-out and no reactive supervisor — and
reporting it in Section V-C (pp. 13–14), Tables 8 and 9 (p. 14). In the static on-route
hazard scenario, KOF reaches a median minimum clearance of **1.73 m** against **1.71 m**
for **KOa** (the keep-out-only ablation, which retains the reactive inspection layer) —
a small observed difference of 2 cm with no statistically detectable difference
(p_Holm = 0.4194) — and spends 9.0 s below the 2 m band against 9.3 s. We do not present
this as established equivalence. The abstract (p. 1) and the conclusion (p. 19) now
state that, **in this scenario, the clearance improvement is attributable to the
detection-triggered keep-out rather than to the reactive weighting**. What the reactive
layer adds over KOF here is the inspection behaviour: 0 of 3 against 3 of 3
(p_Holm = 1.6×10⁻⁴), at 31 s of extra mission time (p_Holm = 0.0021). We present the
pair as a decomposition of the on-route result, and do not extend it to the conflict or
marginal-hazard scenarios, which concern other aspects of the behaviour. We also now
state the calibration of the geometric instruments (Section IV-C, pp. 8–9): both are
entries into regions defined by centre-to-centre distance, with a 0.25 m robot radius,
and the 2 m value is a diagnostic threshold adopted for measuring exposure, not a
requirement the study declares and not a regulatory electrical clearance.

---

**Reviewer#3, Concern # 3:** "Please consolidate the potential-field comparison into one
table … state the baseline's gains, tuning procedure and whether its parameters were
tuned with the same effort … and include the hysteresis and threshold values as a
sensitivity check."

**Author response (implemented):** Agreed on all three.

**Author action:** We updated the manuscript so that a single consolidated table
(Table 10, p. 17) reports mission time, distance, clearance, inspections and
time-to-priority-target with bootstrap intervals. On tuning we give the procedure and
the parameters rather than a characterisation. The APF gains were calibrated so that the
baseline triggers within the same sensing radius as the proposed layer — attraction
crossing its threshold at roughly 4–5 m for waypoints and repulsion at the ≈4.7 m
passage of the beside-route hazard — which was the comparability criterion we applied.
The resulting values are k_att = 1.5, k_rep = 4.0, k_obs = 0.6, with trigger and exit
thresholds of 0.15 and 0.08 on the force magnitude, and a 12 s post-retreat refractory
added against the oscillation that the potential-field formulation is known to exhibit
when a patrol leg passes inside the trigger region. Its approach parameters differ from
ours (1.8 m standoff and a 30 s investigation budget against 2 m and 40 s). These are
reported in the hyperparameter table (Table 4, p. 9) together with the proposed layer's.
Beyond the trigger-range calibration we did not run a further search over these values,
and the time advantage should be read with that in mind; the comparison that *does*
isolate the supervisor on a shared controller is the new heuristic baseline of Section
V-B. We also removed a sentence from the previous version that left a same-controller
heuristic as future work; it is now part of the study.

On sensitivity (Section V-F, p. 16): the three hysteresis pairs separate position from
width — reference (0.45, 0.25), narrower (0.45, 0.35), shifted (0.55, 0.35). Between the
two widths evaluated in the `default` scenario, no difference was detected on any
reported outcome (p ≥ 0.60); shifting the entry point increased the median number of
route deviations from 4 to 8 (p = 0.0003) and reduced the median per-run *total* time
spent in Investigate from 35.1 to 26.6 s (p = 0.0003), while credited inspections
remained three of three. These aggregate measures do not establish that individual
episodes became shorter. We limit the statement to those two widths and that scenario,
and note that the route-deviation metric is sensitive to the entry threshold's position.

---

**Reviewer#3, Concern # 4 (minor):** "Perception is abstracted to oracle events; the
title should not imply a validated autonomous system."

**Author response (implemented):** Agreed.

**Author action:** We updated the manuscript by removing "Autonomous" from the title
(p. 1). More importantly — since removing a word is cosmetic — the abstract (p. 1) and
the conclusion (p. 19) now carry the qualification explicitly: perception is abstracted
to oracle events, the localization transform is held fixed, and the results characterise
the *decision logic*, not a deployable system. The conclusion has a dedicated Scope
paragraph.

---

**Reviewer#3, Concern # 5 (minor):** "Please give the per-configuration counts in the
main text next to the headline numbers, since results such as 4/9 depend on them, and
note whether the exclusion could favour any configuration."

**Author response (implemented):** Agreed, and the second part deserves a direct answer
rather than an assumption of independence.

**Author action:** We updated the manuscript so that valid counts are given in the main
text next to the headline numbers (Section V-J, p. 18) and every rate is reported
against its own denominator. In the earlier battery, n = 10 for every configuration
except APF, KOb, N2 and RHM (n = 9) and DHa (n = 8). In the new battery of 13
configurations, n = 10 for every configuration except three, which are named individually
so the three exclusions can be accounted for without inference: the generic heuristic in
`default` (n = 9), the generic heuristic in `conflict` (n = 9), and the
shifted-hysteresis configuration in `default` (n = 9). These three are the same
start-up failure mode as in the earlier battery, verified rather than assumed: their
recorded travelled distance is ≈1.7×10⁻¹⁶ m. The proposed layer and the
one-factor selection variant retain n = 10 in all three scenarios, which is why the
identity of discrete outcomes reported under Reviewer#2, Concern # 3 is over ten runs
per group.

On bias: all excluded runs inspected zero anomalies, so removing them **raises the
completeness estimate of any block that lost a run — and only those**. We correct here a
statement that was wrong in our previous letter. In `default` the proposed layer has ten
valid runs of ten and averages 3.0 inspections per *attempt*, so the exclusion does not
move it, while APF goes from 2.7 per attempt to 3.0 per valid run; the exclusion
therefore *closes* the per-attempt gap of 0.3 in that pair instead of leaving it
unchanged. The group that does move from 2.7 to 3.0 on the proposed side is RHM, on the
on-route hazard — a different scenario and a different comparator, which we had
conflated. For safety the adjustment runs the *other* way: a run in which the robot never
moved trivially records zero contact-region entries, so including such runs would inflate
the evidence for contact-free navigation, and they are excluded from the safety
statistics too. We do not claim start-up failure is independent of configuration; we
state the direction of each adjustment and report both views.

---

**Reviewer#3, Concern # 6 (minor):** "The response letter appears in the manuscript after
the references, and the template still shows placeholder production metadata; the article
is also long."

**Author response (implemented):** We regret the inconvenience this caused. On
investigation, the appended letter did not originate in the manuscript source — the clean
and highlighted PDFs contain no reviewer text — but in how the files were supplied for the
review package. The remedy is at our end.

**Author action:** The response is uploaded only under *Author's Response Files*, and we
verify the merged review proof page by page before submitting. On the template fields: the
submitted PDF contains no specimen publication dates and no DOI string — `\history` and
`\doi` are called with empty arguments — and the response letter is supplied as a separate
file rather than appended.

On length, we report what moved and what did not, since the comment named three groups.
The **equivalence** material — the η sweep and the η = 0 ablation (Table 14, p. 21,
Appendix B) together with the residual figure (Fig. 7, p. 23, Appendix C) — moved out of
the main text, which also follows from the repositioning. The **dynamic-hazard**
configurations stayed in the main text (Section V-D, p. 14): Reviewer 2 identified that
finding — the keep-out resolves the static hazard while the retreat adds margin only for a
hazard emerging mid-investigation — as a useful architectural observation, and moving it to
an appendix would displace the result that distinguishes the two mechanisms. The
**perception-noise** configurations also stayed (Section V-I, pp. 17–18), because the
confirmation-distance analysis requested in Reviewer#2, Concern # 5 is built on them and
would lose its referent. We acknowledge that the new baseline, the precedence-cost section
and the two retrospective analyses add length; we judged the comments requiring them to take
precedence over net shortening, and kept each addition to the question it answers.

---

**Reviewer#3, Additional question 4 (references on risk-aware navigation and keep-out):**
"The related work on risk-aware and safety-filtered navigation, and on keep-out or
restricted-zone handling in standard navigation stacks, is thin given that the keepout is
the component that carries the safety result."

**Author response (implemented):** Agreed, and the point sharpens under our own new
results: since Section V now attributes the clearance to the keep-out, the gap is more
exposed, not less.

**Author action:** We updated the manuscript by adding Section II-D, *Risk-Aware
Navigation, Safety Filters, and Restricted Zones* (p. 3), which positions our mechanism
against three lines and states what it does and does not provide. Safety filters — control
barrier functions and predictive safety filters — obtain formal guarantees by assuming a
model of the dynamics and of the constraint set. Our precedence rule is a behavioural
arbitration and provides none of those guarantees: it certifies no invariant, and the
marginal-hazard results show it can be over-conservative in a way a filter formulation
would make explicit as a trade-off. Risk-aware planning represents and optimises risk; we
do not, which is why we avoid the term and do not list it among the keywords. Closest to
our mechanism, standard stacks already expose keep-out zones as a map layer, usually
authored statically; our use is the same mechanism driven at runtime by detection. We state
plainly that the contribution is not the keep-out but the measurement of how much of the
safety outcome is due to it, and the arbitration rule governing when the reactive layer
defers. Four references were added for this subsection.

---

We thank the reviewers for helping us clarify the contribution and strengthen its
experimental assessment. The revised manuscript focuses on the evaluated architecture,
reports the absence of a detectable benefit from changing the target-selection criterion in
the tested scenarios, and documents the differences associated with the field-based and
raw-detection triggering modes. It also reports the inspection cost observed under a
marginal hazard, and attributes the clearance improvement in the static on-route scenario to
detection-triggered keep-out handling. The scope and limitations of each comparison are
stated explicitly, both in the responses above and in the manuscript. We thank the Editor
for the opportunity to resubmit.
