# Experimental protocol

The paper links four historical intervention panels to a later evidence audit, then conducts a locally preregistered prompt-only P120 test. These are distinct studies with different denominators. Public statistics are derived from frozen original results; current offline analysis is not an additional Agent experiment.

## Historical intervention panels

| Panel | Intervention and design | Complete-agent observation |
| --- | --- | --- |
| P5 | Rank-16 selective first-edit supervision. Training: 212 units from 97 tasks; validation: 19 units from 10 tasks, partitioned by task and repository. Validation NLL uses 6,888 identical target tokens. A separate 12-task, two-repeat development panel compares BASE and LoRA. | BASE 12/24, LoRA 11/24. The audit separately retains 12 invalid/missing original patch scores as UNKNOWN. Lower target NLL is not a complete-task success metric. |
| P6.2 | A feedback paragraph distinguishes invalid probes from implementation defects. An exploratory 16-task comparison precedes a frozen confirmation on 12 other development tasks, twice each. | Exploration 12/16 → 13/16; confirmation 13/24 for both arms, with two paired wins and two losses. Equal counts are not proof of equivalence. |
| P8 | Eight frozen supplied candidates, six incorrect and two correct. Refinement-only R, generated-check G, and discriminator-oriented D arms each run twice. Extra common budget: eight tools, twelve model requests, 480 seconds. | R/G/D 4/16, 4/16, 3/16. All 32 G/D outputs fail the frozen format gate; no generated independent check executes. All passes preserve initially correct inputs; no initially wrong input is repaired. |
| P12 | Twelve tasks. BASE uses native reasoning history; NH4096 excludes prior thought content while retaining new reasoning; NH1024 also lowers the thinking budget to 1,024. | BASE/NH4096/NH1024 7/12, 7/12, 6/12. These are history-exclusion screens, not learned summarization. |

The historical complete-agent panels generally use Gemma-4-31B QAT deployment, eight minutes, 28 counted tools, 80 turns, and an 8,192-token output cap, with P8's distinct extra refinement budget above. Historical generation seeds were not controlled. P5 trains a BF16-dequantized representation but deploys compressed QAT; this is not exact numerical identity. Panels share tasks and repeats, and should not be pooled as independent tasks. Historical scheduling deviations and a machine migration preclude pooled or cross-hardware efficiency claims.

## E1: mechanical delivery audit

The fixed corpus is P5/P6.2/P8/P12 = 48/48/48/36 episodes: 180 episodes, 2,451 tool events, 21 distinct tasks. Source changes are reconstructed from accepted diffs and tool observations, including source modification via file writes and commands, not just `edit_file`. Semantic intent/relevance labels are secondary.

The strict zero-exit condition requires an executed local check with exit code zero after the **last actual production-source change**. It means at least one qualifying check exists, not that the final check necessarily exited zero, that all requirements were tested, or that runtime-loaded bytes match reconstructed files. UNKNOWN independent scores remain separate. P8's no-new-edit branch can correctly preserve an already-correct supplied patch.

## E4: candidate-conditioned, three-state check comparison

Eligibility was fixed before new replay outcomes. Of 318 candidate-conditioned units, 314 have complete qualified inputs; they correspond to 408 historical check events in 130 episodes. Each fixed check/fixture is evaluated on original source, the actual final candidate, and reference repair, giving 942 canonical CPU executions. Source-preservation and input identity checks qualify the comparison. Four units with incomplete or inconsistent inputs are not silently scored as FAIL.

The public export contains numerical exit states and anonymous historical mappings, **not check bodies or reference implementations**. Unit-level and event-level denominators differ. The main matrix deduplicates check/fixture/candidate/environment identity within panel. Its final-failure condition uses the original independent labels. A separate historical AFTER_LAST_SOURCE_CHANGE event stratum links checks more closely to final delivery; its outputs are still later reexecutions, not model-visible historical feedback. Exit-status non-discrimination does not imply uninformative stdout, agent misbelief, or absent partial coverage.

## Historical source-state alignment

A separate 549-check alignment records conditional reconstructed source identities: 336 match final source and 213 differ. Of 161 episodes with checks, 15 last-check states differ from final source. Later modification is not identical to final mismatch because source may be restored. Print-only checks, caught failures with exit zero, incomplete requirement coverage, and useful checks on old source are separate axes. Historical loaded-module identity was not recovered; do not interpret these numbers as measured rates of agent misjudgment.

## E2/E3: bounded replay, not policy recovery

E2 independently scores reconstructible intermediate and final source states. Twenty qualified tasks yield 166 new final scores, agreeing with all 154 valid comparable original scores; fourteen Selfies episodes remain unqualified. Of 153 attempted intermediate states, 149 obtain valid scores. The Billiard case loses a newly generated passing state; OpenAPI instead loses an initially supplied correct candidate. These are separate bounded existence cases, not an estimated population regression rate. Later qualified scoring does not overwrite historical UNKNOWN records.

E3 applies the original parameters of two budget-denied edits using the official replacement behavior. The P6.2 Pyflakes edit cannot apply because its old anchor is absent. P12 Pyflakes yields a workspace passing 25 tests, but its historical scratch-only submission precedes the denied edit. No continuation, resubmission or end-to-end counterfactual delivery is executed. This is source-edit execution counterfactual evidence, not proof that extra budget rescues the returned artifact. Private task inputs and replacement/scoring code are excluded from the public package.

## P120: prospective exploratory prompt-only test

The local study lock was saved at 2026-11-09 01:48:44 UTC, before the first main run at 02:14:43 UTC. This is a file/hash-pinned local preregistration, **not a public registry or externally timestamped commitment**. The task panel, prompts, seed, contrasts, exposure strata, and UNKNOWN handling were fixed before the 72 main generations. Six exposed engineering smokes are excluded; prompts were not selected by their scores. A host bookkeeping dependency repair before main did not resample smoke Agents or select prompts.

- A: exact Budget-Fit Single Agent V5 baseline.
- B: Stop & Seal budget/closure instructions.
- C: B plus Issue-grounded contract and final-source evidence instructions, termed SEAL.

Only the system prompt differs; model weights, tool interface, and scaffold remain unchanged. Baseline code and prompt text are not redistributed here. The protocol is 24 distinct tasks from 24 repositories × one A/B/C run = **72 actual contemporary Agent generations**, with no historical A reuse. A task's three arms share a physical GPU/profile. All six arm-order permutations occur four times. Twenty-two tasks are reused DEV; two TRAIN-origin candidates have no project-model exposure found in a bounded scan. This is not a 24-task fresh heldout confirmation.

Generation seed is 20261018; temperature 0.2; top-p 0.95; output cap 8,192 tokens; thinking budget 4,096 with thought content retained. Limits: 480 Agent seconds, 28 charged tools, 80 turns, 240 seconds per command. `get_status` and `submit_patch` are uncharged; actual event ordinals and charged budget counts must not be conflated.

Primary contrasts are C−A and C−B; B−A is secondary. Analysis uses paired task flips and unadjusted exact discordant diagnostics. Original outcomes are A 5 PASS/19 FAIL, B 5 PASS/18 FAIL/1 UNKNOWN, C 6 PASS/18 FAIL. C−A has one win and zero losses; original registered C−B net bounds are 0–1 repair. All arms fail the two bounded project-unexposed candidates. The only flip, Abjad, is reused DEV. These observations do not establish stable gain, hidden-score improvement, or prompt-component causality.

The Marshmallow UNKNOWN is preserved in the original view. A later fixed-source CPU diagnosis attributes a duplicate-bound-argument fault to the B candidate; a separate assistant adjudication classifies it FAIL. This creates a 5/5/6 repair view but **not a 72nd strict-valid original score**. The original invalid receipt is not repaired, replaced, or retried.

## Abjad: post-hoc code ablation

After P120, the exact returned C production patch is split into DEFAULT_ONLY and FILTER_ONLY, each applied to the same frozen baseline and scored once with unchanged task inputs/scorer/environment. Default-only yields 8/8 PASS; filtering-only 6 PASS/2 FAIL. This is two CPU patch evaluations, not two new Agent generations or a prompt ablation. See [the case record](../abjad/README.md).

## Semantic review

Rule-assisted annotations and targeted assistant reading are not full manual population annotation. Four historical core claims were reread; two P120 cases reuse prior targeted assistant reviews. Human signatures remain zero. All 72 P120 trajectories have not undergone complete semantic review. Statistical exports do not upgrade these labels or estimate population semantic-label accuracy.
