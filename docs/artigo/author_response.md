**Original Manuscript ID:** Access-2026-33687

**Original Article Title:** "Affective Attraction–Repulsion Value Modulation for
Reactive Inspection Navigation in Electrical Substations"
(revised title: "A Two-Layer Deliberative–Reactive Architecture with an Affective
Attraction–Repulsion Layer for Autonomous Substation Inspection")

**To:** IEEE Access Editor

**Re:** Response to reviewers

Dear Editor,

Thank you for allowing a resubmission of our manuscript, with an opportunity to
address the reviewers' comments.

We are uploading (a) our point-by-point response to the comments (below) (response
to reviewers, under "Author's Response Files"), (b) an updated manuscript with
yellow highlighting indicating changes (as "Highlighted PDF"), and (c) a clean
updated manuscript without highlights ("Main Manuscript").

The reviewers converged on one central point, which we address structurally: in the
tabular instantiation evaluated, the executed behavior is produced by the
threshold-triggered reactive layer on the raw affective field Φ, while the
Bellman-value term ηΦ does not influence any executed action. We realigned the
title, abstract, and claims with the mechanism that actually controls the robot, and
added targeted ablations, an APF baseline, safety scenarios, revised statistical
analyses, and an expanded literature discussion. Where a requested experiment was
not performed, we state this explicitly and treat it as an acknowledged limitation.
All code, data, a per-episode audit trail, a provenance manifest, and checksums are
public under tag `v1.0-resubmission` (commit `8ed4868`).

Best regards,

Milton Miranda Neto et al.

---

**Reviewer#1, Concern # 1:** "If the intention is to retain the present
formulation, the manuscript should avoid implying that the modified Bellman equation
inherits the theoretical properties of standard Q-learning. Alternatively, a
stronger theoretical treatment could establish sufficient conditions under which the
bounded, decaying affective perturbation preserves convergence or characterize how
it alters the fixed point."

**Author response:** We agree and retain the present formulation without claiming any
inherited guarantee. We characterize ηΦ as a bounded, time-decaying additive
perturbation and state explicitly that it is not policy-invariant (Φ is a
single-state, event- and time-dependent potential, not a difference of a state
potential). We do not add sufficient-conditions theory, as the demonstrated
contribution is the two-layer architecture rather than a convergence result.

**Author action:** We updated the manuscript by removing every phrasing implying
inherited Q-learning guarantees, adding the boundedness/decay and non-invariance
characterization in Section III-B (pp. 4–6), and qualifying the abstract (p. 1).

---

**Reviewer#1, Concern # 2:** "Ten runs per configuration are reported, and Welch's
t-test is used… Several metrics are degenerate or nearly so… The revised manuscript
should report effect sizes and confidence intervals and consider exact,
permutation-based, or other distribution-free procedures… the possibility of
inflated type-I error should also be addressed."

**Author response:** We replaced the Welch difference tests with Mann–Whitney U
(exact U distribution for untied small samples; exact permutation p for fully
separated constant groups; tie-corrected normal approximation otherwise), and report
Cliff's δ and a 95% bootstrap confidence interval for the mean difference Δ.
Multiplicity is controlled by Holm correction over the seven principal comparisons;
secondary and directed emerging-hazard comparisons are reported separately and the
latter are exploratory and not Holm-corrected. Per-mission success uses Wilson-score
intervals.

**Author action:** We updated the manuscript by rewriting the statistics in Section
V (pp. 9–10), adding Table 4 (Δ, δ, 95% CI, exact/Holm p-values) and the consolidated
per-pair comparisons in Appendix B (pp. 14–16, Table 10).

---

**Reviewer#1, Concern # 3:** "The adverse scenario… does not establish general
robustness to changing environmental conditions… perturb event locations,
intensities, detection radius, persistence, hazard placement, localization error,
sensor uncertainty, and map geometry. Noise injection would be particularly useful…"

**Author response:** We added a perception-noise sweep (Gaussian on event intensity
and position, two levels) and report the degradation honestly: all three anomalies
are inspected in 10/10 valid moderate-noise runs but in only 4/9 valid high-noise
runs (the losses are confirmation rejections, quantified per episode), while no
entries into the simulated contact region are observed and the mean minimum hazard
clearance increases. Generalization to arbitrary maps, localization drift, event
persistence, and physical perception is not demonstrated and is stated as an
acknowledged limitation.

**Author action:** We updated the manuscript by adding the perception-noise analysis
(Sections V-F/V-H, p. 13; Table 8) and stating the remaining generality limits under
threats to validity (p. 14).

---

**Reviewer#1, Concern # 4:** "One trajectory cannot establish convergence… include
TD-error trajectories from all runs, or at least aggregated convergence statistics
with uncertainty. It would also be useful to compare the proposed update against
ordinary tabular Q-learning…"

**Author response:** The submitted convergence metric excluded the affective term by
construction. We now log the complete update residual |αδ + ηΦ| and aggregate it over
all ten valid E3 runs after resampling onto a common normalized mission-time grid;
Figure 7 shows the across-run mean and the 2.5th–97.5th percentile band (inter-run
spread, not a confidence interval for the mean). Table 5 also reports the residual
for E0 (η = 0), the arm without the affective term; this is not a comparison between
learned policies controlling the robot. We reword the claim to empirical stability of
finite-run increments and make no convergence claim.

**Author action:** We updated the manuscript by replacing Figure 7 with the
aggregated complete-residual figure (Section V-G, p. 13), reporting the E0 residual
(Table 5, p. 11), and rewording the stability statement.

---

**Reviewer#1, Concern # 5:** "…the literature synthesis does not yet reflect the
breadth of contemporary work on substation robotics and learning-based navigation…
position your method against these approaches using a concise comparative table…"

**Author response:** We expanded the related-work discussion to 21 references
(substation robotics including DRL and ant-colony planning and PPO/DDQN/A*
comparisons, active perception and informative path planning, safe RL,
potential-based shaping, behavior arbitration, and hybrid deliberative–reactive
control), and added a comparison table.

**Author action:** We updated the manuscript by expanding Section II (p. 3) and
adding the comparison table (Table 1, p. 4), with the new references at p. 15.

---

**Reviewer#1, Concern # 6:** "…the reported mission-time result… E3 increases
travelled distance from ≈72 m to >86 m, E5 ≈91.5 m… analyze as part of the mission
trade-off… inspection success per additional meter, inspection time per event,
safety clearance, and total mission utility…"

**Author response:** With the corrected instrumentation, the baseline (320 s,
80.4 m) is faster and shorter than the method (364 s, 86.6 m; E5 397 s, 92.2 m); we
report this as a bounded, measured cost, jointly with inspection completion and
safety clearance. Relative to E1, E3 adds about 6.2 m and 44 s for three additional
inspections — about 2 m and 15 s per additional inspected anomaly (aggregate marginal
mission costs, not per-target dwell durations). The method is more time-efficient
than the APF baseline (404 s).

**Author action:** We updated the manuscript by adding the mission trade-off
analysis in Section V-E (p. 12) and correcting the earlier "no significant increase"
wording (abstract, p. 1).

---

**Reviewer#1, Concern # 7:** "…the distinction between the affective state machine
and the Bellman-value modification should be explicit… value-update stability… would
benefit from qualification because the evidence is empirical…"

**Author response:** The abstract now separates the FSM from the value modification,
qualifies stability as empirical, states completeness numerically (9/10 dense, 4/9
high noise), and describes safety as observed contacts and measured margins rather
than a general guarantee.

**Author action:** We updated the manuscript by rewriting the abstract (p. 1).

---

**Reviewer#2, Concern # 1:** "The principal Bellman-update contribution is not
demonstrated… Please explain (a) how actions are selected from Q; (b) whether an
ε-greedy or another exploration policy is used; (c) how these discrete actions relate
to Nav2/MPPI velocity commands; (d) when and how often Q is updated; and (e) what
observable behavior changes when the ηΦ term is removed… At minimum, a Nav2 + FSM
without the Q-learning term ablation is required."

**Author response:** Q does not select executed actions. (a) The action associated
with each observed transition is inferred from odometry — no greedy action is sent to
the base; (b) no exploration policy acts on the robot; (c) the discrete Q-table
actions are not mapped to Nav2/MPPI commands, which come from patrol/inspection/
retreat goals; (d) the table is updated from consecutive odometry observations; (e)
removing ηΦ changes no executed action. E0 retains Stay Alert and sets η = 0,
removing the affective value term while retaining the passive TD update — it is an
ablation of ηΦ, not an experiment with the Q node disabled.

**Author action:** We updated the manuscript by adding the "what the value table does
and does not control" paragraph and the E0 ablation column (Section III-B, p. 6;
Tables 5 and 10).

---

**Reviewer#2, Concern # 2:** "The distinction between the proposed update and reward
shaping is not adequately established… affective information appears in both r and
ηΦ… provide a rigorous derivation… explain the attraction/repulsion asymmetry…
Claims of novelty relative to reward shaping should be moderated…"

**Author response:** We removed the affective component from the reward, retaining the
progress reward, so that Φ enters once through ηΦ (attraction and repulsion are now
symmetric). We derive that, for fixed α, the external ηΦ term is equivalent to
augmenting the reward by ηΦ/α, and make the comparison to potential-based shaping
explicit, noting where our term departs from a policy-invariant potential. Novelty is
claimed for the architecture, not for the update as a distinct RL operator.

**Author action:** We updated the manuscript by adding the reward-shaping derivation
and de-duplicating the reward (Section III-B, pp. 5–6), and moderating the novelty
statement.

---

**Reviewer#2, Concern # 3:** "The effect of η is not tested meaningfully… Please
either (a) connect Q and η to the executed navigation policy and repeat the sweep; or
(b) present the current sweep only as a numerical analysis of the Q table… A factorial
experiment that independently enables and disables the FSM and Bellman term would
clarify the contribution of each component."

**Author response:** We adopt option (b): the η sweep is a numerical analysis of the
passive value table. E0 and E3 have identical observed inspection counts, and their
mean mission times are equivalent within the ±5 s TOST margin (Table 10); this does
not establish equivalence of every behavioral metric or trajectory. We did not
conduct a full FSM × value-update factorial experiment; instead we document the
control architecture and report the targeted η = 0 ablation, which is sufficient
because η has no path to executed control.

**Author action:** We updated the manuscript by re-scoping the η sweep to a Q-table
analysis (Section III-B, p. 6; Section V-E, p. 12; Appendix B).

---

**Reviewer#2, Concern # 4:** "The value-function stability claim is not supported by
the reported metric… the TD-error proxy excludes the affective term… Figure 7 presents
only one representative run… Please calculate the complete update residual, including
ηΦ, across all runs with uncertainty… 'stable during the evaluated simulations' would
be more defensible than 'convergent.'"

**Author response:** Addressed together with Concern 1.4: the complete residual
|αδ + ηΦ| is aggregated over all ten valid E3 runs (inter-run 2.5th–97.5th percentile
band), the wording is "empirical stability," and we discuss why tabular-Q convergence
assumptions do not apply to a time-varying, decaying, event-dependent Φ.

**Author action:** We updated the manuscript by adding the complete-residual figure
and the assumptions discussion (Section V-G, p. 13; Table 5, p. 11).

---

**Reviewer#2, Concern # 5:** "Stronger and fairer baselines are needed… compare
against (a) Nav2 plus the same FSM without Q-learning; (b) a conventional
artificial-potential-field or local reactive method; (c) conventional
reward-augmented Q-learning; and (d) where feasible, a recent learning-based reactive
navigation method."

**Author response:** We added (a) the η = 0 ablation (E0) and (b) an
artificial-potential-field controller (APF) on the same events. We did not include
(c) an actuating reward-augmented Q-learning baseline or (d) a recent learned
reactive navigator: implementing and training such policies is outside the revised
scope, which evaluates reactive supervision rather than learned action selection, so
we make no claim of superiority over these missing baselines. The APF comparison
evaluates the released APF implementation, which differs in controller and approach
parameters. A heuristic supervisor using the same Nav2/MPPI controller to isolate the
affective weighting's contribution also remains an explicit limitation.

**Author action:** We updated the manuscript by adding the E0 and APF configurations
and the keepout/retreat ablation (Tables 3 and 5, pp. 9 and 11; Section V-E, p. 12),
and stating the missing (c)/(d) baselines and the same-controller heuristic as
explicit limitations.

---

**Reviewer#2, Concern # 6:** "The safety claim is presently weak… the minimum hazard
distance is not significantly improved… the hazard is positioned beside rather than
across the planned path. Please test hazards that intersect or dynamically intrude
upon the route and report collision rate, safety-zone violations, time below a
specified clearance, minimum time-to-collision, retreat success rate, and mission
recovery."

**Author response:** We add a hazard placed on a patrol leg; there the method (RHM)
contours at a 1.71 m minimum clearance versus the baseline's 0.71 m (RHB). A
keepout/retreat ablation shows the deliberative keepout resolves the static hazard
(the retreat alone oscillates), and a directed, exploratory emerging-hazard trial
(DHa n = 8, DHb n = 10) isolates the reactive retreat's transient margin (+0.33 m),
accompanied by greater time and distance and a deferred inspection (its TTC is a
whole-mission minimum, not a post-activation statistic). We report safety as observed
outcomes — no entries into the simulated contact region (centre-to-centre distance
below 0.5 m) were observed in the valid runs — and measured margins under finite
samples, not a general guarantee.

**Author action:** We updated the manuscript by adding the hazard-on-route,
keepout/retreat, and emerging-hazard results with the requested safety outcomes
(Sections V-B–V-D, pp. 10–12; Tables 6, 7, and 10).

---

**Reviewer#2, Concern # 7:** "The statistical analysis requires strengthening…
provide (a) the exact comparison for every p-value; (b) exact p-values; (c) effect
sizes and 95% confidence intervals; (d) a multiplicity-control procedure; (e) methods
appropriate for bounded counts or success proportions; and (f) sensitivity results
with and without the two timeout runs. Raw per-run results should also be provided."

**Author response:** Items (a)–(e) are addressed as in Concern 1.2. Regarding (f), we
do not present a with/without sensitivity reanalysis of the two original-submission
timeout runs: the revised results use the corrected evaluation battery, for which we
report performance conditional on the movement criterion separately from six immobile
attempts. These six are not the two original mid-mission timeouts; their observable
exclusion criterion and per-run records are provided, and the 154/160
movement-qualified fraction is reported separately from inspection and navigation
performance. Raw per-run CSVs and a per-episode audit trail are public.

**Author action:** We updated the manuscript by adding the full statistical treatment
and the movement-qualified reliability outcome, and releasing the per-run data and
audit trail (Section V, p. 9; Section V-I, p. 14; Appendix B).

---

**Reviewer#2, Concern # 8:** "The event and inspection definitions require
clarification… clarify whether 'anomalies inspected' counts committed or
reached-and-dwelled targets… Detection, investigation initiated, inspection
completed, and timeout should be reported as separate outcomes. The arbitration rule
in Equation (4) also needs clarification… tie handling, target identity retention,
switching behavior, and how hazard priority interacts with magnitude-based selection."

**Author response:** Detection, committed (investigation initiated), completed
(reached + commanded dwell + independent pose confirmation within a stated distance of
the true target), timeout, navigation failure, and hazard-deferral are now separate
outcomes; "anomalies inspected" counts only confirmed completions, named a proxy. The
original signed-selection rule (formerly Eq. (4)) is replaced by the two-channel
formulation in Eqs. (4)–(7); Eq. (7) gives the hazard channel precedence whenever
h > ε (distinct from the FSM threshold Φ ≤ −θ_in and its additional Avoid
conditions), Eq. (5) specifies attraction selection and tie-breaking by smallest
event identity, and Eq. (6) describes decay.

**Author action:** We updated the manuscript by separating the outcome definitions and
reformalizing the field (Sections III-B/III-C, pp. 5–6) and documenting them in the
per-episode audit trail (Section IV-D, p. 9).

---

**Reviewer#2, Concern # 9:** "Several statements should be corrected or moderated…
'Stay Alert inspects all anomalies' is not true for every configuration (E2 2.7 ± 0.9)…
'At no significant increase in mission time' should identify the comparison and not be
read as equivalence… 'Detection scales to denser layouts' is too strong."

**Author response:** "Inspects all anomalies" is qualified to the default scenario and
moderate noise (in the revised battery E2 is 3.0 ± 0.0; completeness is 9/10 dense and
4/9 high noise, stated explicitly). "No significant increase in mission time" is
replaced by a measured cost; the scaling claim is softened to the single dense
scenario tested.

**Author action:** We updated the manuscript by qualifying these statements in the
abstract (p. 1), Sections V-F/V-H (p. 13), and the conclusion (p. 14).

---

**Reviewer#2, Concern # 10:** "The literature review is too limited for the breadth of
the novelty claim. Only 14 references are provided, including two arXiv entries… The
statement 'to our knowledge' should be supported…"

**Author response:** Addressed as in Concern 1.5 (21 references, comparison table; the
two former arXiv entries are now cited by their published conference versions). The
novelty claim is delimited to the declared scope and contextualized by the expanded
review; the remaining "we are not aware of a prior method…" statement is scoped to
this setting rather than asserted globally.

**Author action:** We updated the manuscript by expanding the review and comparison
table (Section II, p. 3; Table 1, p. 4) and scoping the novelty statement.

---

**Reviewer#2, Minor Concern # 1:** "Equation (3) gives an intensity of Ie/2 at d = R,
followed by an abrupt disappearance beyond R. Please justify this profile and test
sensitivity to the detection model."

**Author response:** The range-dependent profile is retained: Eq. (3) gives an
intensity of I_e/2 at d = R, and the event is not reported beyond R. We now explicitly
acknowledge this boundary discontinuity and explain how the distinct enter/exit
thresholds and episode commitment prevent repeated reactive transitions, and we report
sensitivity to event-position and intensity noise. We did not perform a dedicated
detection-radius sweep and do not claim the profile is continuous at R.

**Author action:** We updated the manuscript by adding the boundary/hysteresis
explanation (Section III-B, p. 5) and the noise sensitivity (Section V-H, p. 13), and
by removing the earlier promise of a detection-radius sweep.

---

**Reviewer#2, Minor Concern # 2:** "The notation in Equation (4), particularly the
signed argmax-by-magnitude operation, should be rewritten more formally."

**Author response:** The signed selection is written formally within the two-channel
formulation (Eqs. (4)–(7)), with explicit tie-breaking by smallest event identity and
the empty-set per-channel behavior.

**Author action:** We updated the manuscript by reformalizing the selection in Section
III-B (p. 5).

---

**Reviewer#2, Minor Concern # 3:** "Φ is written as Φ(s,a), but the field calculation
appears to depend on event modality, intensity, and distance rather than on action a.
Define the action dependence explicitly or revise the notation."

**Author response:** Φ is an action-independent field of event modality, intensity,
and distance; we revised the notation accordingly and note a memory approximation
rather than a full Markovian claim.

**Author action:** We updated the manuscript by correcting the field notation (Section
III-B, pp. 5–6).

---

**Reviewer#2, Minor Concern # 4:** "Explain why the baseline Q TD-error is reported as
zero and whether Q-learning is disabled or merely unlogged in E1."

**Author response:** In the baseline the value node is inactive, so no update occurs
and the residual is identically zero.

**Author action:** We updated the manuscript by stating this (Section IV-C, p. 8;
Table 5 caption, p. 11).

---

**Reviewer#2, Minor Concern # 5:** "Please report random seeds, initialization rules,
simulator real-time factor, computing hardware, software commit identifier, and the
precise code version used to generate the submitted results."

**Author response:** The recorded seeds pertain to the per-repetition
perception-noise generator (the run index passed as seed and recorded in each CSV);
the remaining run-to-run variation is physics and navigation-stack timing, which a
single seed does not control. We report initialization rules, real-time factor,
hardware, and the exact commit, and release the audit trail, provenance manifest, and
checksums.

**Author action:** We updated the manuscript by adding these reproducibility details
(Section IV-D, pp. 8–9; Table 3, p. 9) and the tagged release.

---

**Reviewer#2, Minor Concern # 6:** "Verify the final production metadata. The template
still displays 'Submitted…; revised…; accepted…,' an apparent placeholder DOI, and
'VOLUME 11, 2023.'"

**Author response:** The template placeholders (history line, DOI, volume/year) are
zeroed to mark the manuscript as a draft; we do not represent this as satisfying all
of the journal's production requirements.

**Author action:** We updated the manuscript by zeroing the placeholder metadata on
the first page and footer.

---

**Reviewer#3, Concern # 1:** "The actual robot behavior seems triggered by the
threshold-based affective field Φ. Please clarify clearly what additional benefit is
brought by Bellman value modulation itself."

**Author response:** In the tabular instantiation, the immediate benefit is delivered
by the reactive layer; the value modulation is a formulation/substrate for future
learned policies — shown numerically stable but not the driver of the reported
behavior. The title, abstract, and contributions reflect this.

**Author action:** We updated the manuscript by reframing the contribution (abstract,
p. 1; contributions, p. 2; Section III-B, pp. 4–6).

---

**Reviewer#3, Concern # 2:** "The safety evaluation could be slightly strengthened…
the minimum hazard distance is not significantly improved over the baseline. A simple
case with the hazard directly on the patrol route may better demonstrate the
advantage."

**Author response:** We added the hazard-on-route scenario (RHM 1.71 m vs RHB 0.71 m),
a keepout/retreat ablation, and a directed emerging-hazard trial, with safety outcomes
reported (see Concern 2.6).

**Author action:** We updated the manuscript by adding these scenarios and results
(Sections V-B–V-D, pp. 10–12; Tables 6, 7).

---

**Reviewer#3, Concern # 3:** "Fig. 7 shows one representative TD-error curve. It may be
better to describe this as empirical stability rather than convergence, unless more
evidence is provided."

**Author response:** Agreed; the figure and wording report empirical stability of the
value increments over the ten valid E3 runs, with no convergence claim, and aggregate
the complete residual (see Concern 1.4).

**Author action:** We updated the manuscript by revising Figure 7 and its description
(Section V-G, p. 13).

---

**Reviewer#4, Concern # 1:** "The value-update term is the contribution named in the
title, but the experiments do not test it… Please add a run with eta = 0 and Stay
Alert enabled. If it reproduces E3, the value-update formulation should be presented as
a design proposal for future learned policies, and the title, the abstract and the
second contribution bullet adjusted to match."

**Author response:** Implemented as suggested for the specific η = 0 request: the η = 0
run (E0) reproduces the method's observed behavior, and we present the value update as
a design proposal for future learned policies.

**Author action:** We updated the manuscript by adding the E0 configuration and
adjusting the title, abstract, and second contribution bullet (title and abstract,
p. 1; contributions, p. 2; Section V-E, p. 12).

---

**Reviewer#4, Concern # 2:** "The baseline cannot inspect anomalies by construction, so
the headline comparison carries little information… A comparison against a reactive
scheme of similar simplicity would be more useful, for example the artificial potential
field of [10] or a plain detour-on-detection heuristic without the value term, run on
the same events."

**Author response:** We added an artificial-potential-field controller and the η = 0
(no-value) ablation on the same events, plus a keepout/retreat ablation. A heuristic
supervisor using the same Nav2/MPPI controller — which would isolate the affective
weighting's specific contribution — remains an explicit limitation rather than a claim.

**Author action:** We updated the manuscript by adding the APF and E0 configurations
(Tables 3 and 5, pp. 9 and 11; Section V-E, p. 12) and stating the same-controller
heuristic as a limitation.

---

**Reviewer#4, Concern # 3:** "The safety claim is stronger than the evidence… Either
soften those statements or add a scenario with a hazard on a patrol leg… the adverse
scenario is described as requiring arbitration between clustered events, but Eq. (4)
keeps only the single largest contribution and the hazard at (2, −13) is far from both
anomaly clusters, so no attraction against repulsion conflict is ever exercised."

**Author response:** We add a hazard on a patrol leg and a conflict scenario in which
an anomaly and a hazard are co-located and both in range, so the field's arbitration
is genuinely exercised (the hazard-first precedence preempts the more salient anomaly).
Safety statements are softened to a consistent maneuver and measured margins rather
than a larger incidental clearance or a general guarantee.

**Author action:** We updated the manuscript by adding the on-route and conflict
scenarios and softening the safety claims (Sections V-C/V-D, pp. 11–12; Table 10;
abstract and conclusion).

---

**Reviewer#4, Minor points:** "In Eq. (3) the intensity is 0.5 I_e at d = R and zero
beyond, so Phi jumps at the detection boundary… Several Welch tests compare groups with
zero variance in both arms… where the reported p values are not meaningful… The figure
list in the Acknowledgment is out of order (Figs. 4, 6, 5, and 7)."

**Author response:** The Eq. (3) boundary is now explained rather than removed (see
Minor Concern 2.1); the zero-variance Welch comparisons are replaced by count
differences with exact tests and effect sizes (see Concerns 1.2/2.7); the
Acknowledgment figure order is corrected.

**Author action:** We updated the manuscript by explaining the Eq. (3) boundary
(Section III-B, p. 5), replacing the degenerate tests (Section V; Table 4), and
correcting the Acknowledgment figure order (p. 15).

---

*Note: References suggested by reviewers have been added only where relevant and where
they strengthen the article; the two previously-cited arXiv preprints are now cited by
their published conference versions.*
