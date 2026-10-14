# Cover Letter — IEEE Access (Revised Resubmission)

To the Editor-in-Chief
*IEEE Access*

**Manuscript title:** A Two-Layer Deliberative–Reactive Architecture with an Affective Attraction–Repulsion Layer for Autonomous Substation Inspection

**Previous manuscript ID:** Access-2026-33687

**Manuscript type:** Research Article

**Corresponding author:** Milton Miranda Neto, Faculty of Electrical Engineering, Universidade Federal de Uberlândia (UFU), Uberlândia, MG, Brazil (e-mail: voidmmn@ufu.br)

---

Dear Editor,

We are pleased to submit a thoroughly revised version of our manuscript, previously
"Affective Attraction–Repulsion Value Modulation for Reactive Inspection Navigation in
Electrical Substations" (Access-2026-33687), now retitled **"A Two-Layer
Deliberative–Reactive Architecture with an Affective Attraction–Repulsion Layer for
Autonomous Substation Inspection,"** for consideration as a Research Article. A
detailed, point-by-point response to the four reviewers accompanies this submission.

Autonomous inspection of electrical substations is typically handled either as a
fixed-coverage patrol, which classifies whatever appears without adapting its motion to
what it senses, or by purely reactive controllers, which respond only to stimuli
already within sensor range. Our work bridges these regimes with a two-layer method: a
deliberative active-sensing patrol, built on a standard, reproducible industrial stack
(ROS 2, Nav2 with an MPPI controller, Gazebo Fortress), carries the sensors to where
events may occur, while a reactive *affective* layer — Stay Alert — makes the robot
approach anomalies to inspect them and retreat from hazards, arbitrated by a
hazard-first attraction/repulsion field.

**The reviewers converged on one central point, which we have addressed structurally
rather than cosmetically.** In the tabular instantiation evaluated, the executed
behavior is produced by the threshold-triggered reactive layer on the raw affective
field, while the Bellman-value term does not influence any executed action. We have
realigned the paper's title, abstract, and claims with the mechanism that actually
controls the robot, and we present the value update as a formulation and substrate for
future learned policies rather than as the behavior driver. This reframing is a
concession the evidence required, and we make it explicitly.

We believe the revised manuscript is a good fit for *IEEE Access* for three reasons:

1. **A validated, honestly bounded contribution.** Across a uniform battery of sixteen
   configurations, the fixed baseline inspects no off-route anomalies, whereas the
   proposed layer inspects all three in the default scenario and under moderate noise,
   and consistently performs the hazard-avoidance maneuver. We report the method's
   limits with the same care: completeness degrades under dense clustering (9/10 runs
   complete all five events) and under high perception noise (4/9), while no
   contact-region entries (zero collisions) were observed in any scenario. On a hazard
   placed on the patrol route, the method contours at a 1.71 m minimum clearance versus
   the baseline's 0.71 m, and a keepout/retreat ablation identifies the deliberative
   keepout as the mechanism that resolves the static hazard; a directed emerging-hazard
   trial isolates the reactive retreat's transient safety margin, with its cost stated.

2. **Reproducibility and technical soundness.** The method runs on a standard, openly
   available stack, and the complete code, simulation world, launch files, batch runner,
   and analysis scripts are released publicly under a tagged release, together with the
   per-run data, a per-episode audit trail, a provenance manifest, and file checksums.
   The evaluation uses distribution-free statistics (Mann–Whitney U, Cliff's δ, bootstrap
   confidence intervals, Holm correction, and equivalence testing) appropriate to the
   bounded-count and constant-variance outcomes the reviewers flagged.

3. **Transparent empirical reporting.** We state the boundary of the value term
   explicitly, correct the earlier overstatements the reviewers identified (mission time
   is a measured cost, not "no significant increase"; completeness is qualified, not
   universal; safety is reported as observed contacts and measured margins, not a general
   guarantee), and we are candid about the remaining limitations — chiefly that the
   demonstrated originality is that of integration and analysis, since we do not isolate
   the affective weighting against a heuristic supervisor using the same controller, and
   that validation is in simulation.

We confirm that this manuscript is original, has not been published previously, and is
not under consideration for publication elsewhere. All authors have approved the
submission and meet the IEEE authorship criteria. We have no conflicts of interest to
declare. In accordance with IEEE policy, the use of AI-based tools in the preparation of
this manuscript (for two conceptual figures and for assistance with text and
analysis-script editing) is disclosed in the Acknowledgment section; the authors have
reviewed and verified all such content and take full responsibility for it.

We thank the Editor and the reviewers for an unusually careful and constructive review,
which materially improved the work, and we look forward to your decision.

Sincerely,

Milton Miranda Neto, on behalf of the authors
Universidade Federal de Uberlândia (UFU)
voidmmn@ufu.br
