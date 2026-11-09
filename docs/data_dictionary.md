# Minimal public numerical data

The release contains factual numerical projections, not task implementations or executable checks. `python3 scripts/verify_statistics.py --output results.json` recomputes the three main tables, Figure 2, P120 paired outcomes and the Abjad Figure 3 values with the Python standard library (Python 3.11 or newer). The input directory is read-only to the script; the optional output must be outside `data/`. It does not import task packages, load a model, access a GPU or network, or invoke a task scorer.

## Identifiers and dependence

Task identifiers `Tnnn` are stable across the historical and P120 projections. The historical corpus has **21 distinct tasks**; P120 has **24 distinct tasks/repositories**. These sets overlap. Opaque IDs preserve that overlap without publishing the complete task list. They are pseudonymous, linkable identifiers, not a guarantee of anonymity. The selected Abjad case is explicitly named through `public_case: Abjad`; no other task identity mapping is exported.

Historical episodes use `Hnnn`, qualified check/candidate units `Unnn`, retained historical check mappings `Knnn`, P120 model cells `Mnnn`, and P120 repositories `Rnnn`. Repeats and panels share tasks. Units and historical mappings have different denominators; never pool episode or unit rows as independent tasks or attach independence-based confidence intervals to their sums.

## `historical.json`

This file contains 180 episode rows, 716 necessary numeric source-change/check-event rows, 314 qualified three-state check/candidate units with 408 historical mappings, and the numerical inputs needed for the historical intervention table. The 1,735 other tool events contribute neither a source change nor an executed check and are omitted; each episode retains its original event count, whose sum recovers the paper's 2,451-event corpus size.

| Object / field | Meaning |
| --- | --- |
| `episodes[].episode_id`, `panel`, `task_id`, `arm` | Anonymous joins; panels P5, P6.2, P8 and P12 remain separate. |
| `historical_resolved` | Recorded historical complete-agent resolution used for Table 1. Scheduled attempts remain in the denominator, including attempts without a valid independent patch score. |
| `original_event_count` | Number of all retained original tool events for this episode, including the omitted non-source/non-check rows. These 180 counts sum to 2,451. |
| `score_valid`, `final_resolved` | Original independent-scoring validity and nullable result used for Table 2. `final_resolved: null` is UNKNOWN, not FAIL. These fields are not replaced with later replay labels. |
| `events[].position` | Historical order within an episode. No command text, arguments or feedback are distributed. |
| `source_changed` | Mechanically reconstructed actual production-source change, including supported non-`edit_file` writers. A tool call alone is not a change. |
| `test_executed`, `exit_code` | Whether the event executed a retained local check, and its process exit status. Exit zero is not a verified successful test or proof of Issue coverage. |
| `candidate_units[].unit_id` | A qualified, frozen unit deduplicating check/fixture/candidate/environment identity. Qualification precedes the new state-execution outcomes. |
| `frozen_unit_identity_sha256` | Opaque digest of that identity. It is not a task snapshot or executable test. |
| `raw_receipt_sha256`, `source_tree_sha256` | Digests of the original saved numeric receipt and original/candidate/reference production-source identity records; their underlying code and receipts are not redistributed here. |
| `exits` | Existing offline check exit codes on original buggy source, actual final candidate, and reference repair. They are not new Agent runs or historical feedback observed by the model. |
| `source_preservation_qualified` | Existing qualification that fixed-check execution retained the intended production source. All 314 exported units qualify. |
| `historical_mappings[]` | Anonymous historical episode/check-event association, panel, timing, and original final-score validity/result. These associate one qualified unit with possibly repeated historical checks. |
| `historical_timing` | Position relative to production edits. `AFTER_LAST_SOURCE_CHANGE` forms the event-weighted terminal subset; the full unit subset may include pre-edit or intermediate checks. |
| `loss_units[]` | Nineteen anonymous validation units: `n_loss`, total baseline NLL, total LoRA NLL. Sum total NLL and divide by the same 6,888 target tokens; do not average per-unit means. |
| `feedback_exploration` | Historical exploration PASS/scheduled counts, separate from frozen feedback confirmation. |
| `native_history_tokens` | Input/output token totals per P12 arm; input reductions use BASE input total as denominator. No cross-hardware timing estimate is implied. |
| `generated_check_gate` | P8 independent-check generation and actual execution counts: 32 generated, zero executed. This is an interface failure, not evidence about usable check feedback. |

### Figure 2 and Table 2

The script finds each episode's last actual production-source change. A strict local check exists only if a retained executed check exits zero at a **later** position. This is an existence condition, not a claim that the final check was zero or that the final version passed an Issue oracle.

`figure2` contains per-panel `source_changed`, `strict_post_last_change_zero`, and `resolved_inside_strict`, plus denominators and score-validity diagnostics. `figure2_episode_subsets` provides the 180 underlying membership records. These are nested descriptive subsets, not a necessary route for every success: P8 can correctly preserve a supplied candidate without making a new source edit.

### Table 3

`candidate_zero_units` conditions on historical final FAIL and deduplicates qualified units within panel. `all_three_zero_among_candidate_zero` conditions further on candidate exit zero. `post_last_change_candidate_zero_events` instead counts historical mappings after the last production-source change, not deduplicated units. Full-subset and terminal-subset ratios therefore have distinct units of analysis. All are existing offline reexecutions, not measured rates of historical Agent misbelief. Identical exit status may coexist with informative different stdout, which is intentionally not distributed.

## `p120.json` and `p120_adjudication.json`

`p120.json` contains exactly 72 original contemporary main model cells, one A/B/C triplet on each of 24 tasks. Six exposed engineering smokes are excluded. Original outcomes are A 5 PASS/19 FAIL, B 5 PASS/18 FAIL/1 UNKNOWN, C 6 PASS/18 FAIL. The original UNKNOWN is preserved.

`exposure_stratum` retains the frozen two-candidate versus 22 reused-DEV split. The two candidates had no project-model exposure found in the bounded audit; this does not establish universal non-exposure or a fresh 24-task heldout panel. All three arms failed both candidates.

`frozen_protocol` is a whitelist projection of the local pre-main study lock: unchanged model, seed, sampling, budgets, uncounted tools, arm-order permutations and prespecified contrasts. The local hash-pinned lock is not a public preregistration registry. The protocol is descriptive; this release cannot execute that model experiment.

`p120_adjudication.json` contains one separate post-hoc assistant source-attribution decision: UNKNOWN → candidate FAIL. It creates no new valid scoring receipt and does not modify the original outcome rows. The script emits `p120.original` and `p120.posthoc_source_adjudicated` separately, together with paired wins/losses and registered net bounds for UNKNOWNs. The exact discordant diagnostic is unadjusted and exploratory; a single flip does not establish stable gain or prompt causality. Exposure-stratum outputs preserve both result views.

## `abjad_results.json`

This independently documented file separates three original A/B/C Agent-score summaries from two subsequent CPU patch-ablation summaries. The script emits those results and the observed timeline as `abjad_figure3`. The two ablations are not added to the 72 Agent generations. Source record, patch, environment and scorer digests identify saved provenance without distributing a private scoring harness or tests. See the Abjad documentation for its original C score source and limits.

## `provenance.json` and verification boundaries

`source_files` gives logical labels and SHA256 digests of original frozen numerical inputs. The raw source files are deliberately excluded. These digests identify provenance but do not make the excluded sources publicly accessible or independently prove their contents. The private export audit records the complete field mapping and verifies the source bytes unchanged.

`export_files` gives SHA256 digests of the public data projections, including the independently prepared Abjad summary and the aggregate supplement. The public script verifies these distributed bytes before calculating statistics. This is a consistency check, not a cryptographic attestation by an external registry. All data files can be inspected directly as JSON.

## `supplementary_counts.json`

This small whitelist projection retains four panel-level source-state-alignment summaries: `check_events`, `episodes_with_checks`, `check_source_differs_from_archived_final`, and `[mismatched episodes, episodes with checks]` for the last-check state. The script sums them to 549 checks, 213 source/final differences and 15/161 last-check mismatches. It does not reconstruct the excluded check bodies or loaded runtime bytes.

The same file retains numerical E2 completion/coverage counts, the E3 submit-before-denied-edit chronology and fixed-test count, and targeted semantic-review counts, each tied to logical source IDs and original SHA256 provenance. These are **retained frozen aggregate summaries**, not a claim that the public script reruns source-state replay, regrades a patch, or individually reconstructs the underlying cases and semantic judgments. The script exposes them under `supplementary.retained_aggregate_summaries`; it newly sums only the published state-alignment panel counts.

The verification command promises recomputation of the target tables, Figures 2/3 and the specified numerical supplement. It does not claim to independently reconstruct every protocol or narrative number in the manuscript. Other retained manuscript details are traceable through the frozen parent-manuscript hash and documented publication provenance.

Excluded throughout: task Issue text and hints, commands and tool arguments, stdout/stderr, private tests and fixtures, scoring implementations, complete source snapshots, model/API archives, credentials, personal information, host paths and private-repository URLs. No raw source-code content appears in these statistical JSON files.
