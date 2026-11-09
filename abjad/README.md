# Abjad: three patches, two later CPU ablations, one original C score

This case concerns the public upstream repository [Abjad/abjad-ext-nauert](https://github.com/Abjad/abjad-ext-nauert), issue 24, at base commit `520f389f06e21ee0a094016b4f1e2b0cb58263c1`. Only three narrow production-code patches and sanitized numerical receipts are redistributed. No task snapshot, test body, private scorer, API archive, scratch reproduction script, or private Git history is included.

| Patch | Origin | Existing frozen-test outcome |
| --- | --- | --- |
| [`FULL_C.patch`](patches/FULL_C.patch) | Exact returned C patch from one of the original 72 P120 Agent generations | 8 PASS / 0 FAIL |
| [`DEFAULT_ONLY.patch`](patches/DEFAULT_ONLY.patch) | Post-hoc CPU ablation: only constructor default False → True | 8 PASS / 0 FAIL |
| [`FILTER_ONLY.patch`](patches/FILTER_ONLY.patch) | Post-hoc CPU ablation: only replace mutation-during-iteration with filtering | 6 PASS / 2 FAIL |

The two ablations were each scored once, after the main Agent campaign, using the same frozen scorer, task snapshot, environment receipt/fingerprint, and official baseline tree as original C. These are **two later CPU scoring executions, not two additional Agent experiments**. Current publication-time statistical recomputation adds neither Agent generations nor new scoring executions.

## What the ablation identifies

Changing the default alone suffices to reproduce original C's PASS on the existing eight-test evaluation. Filtering alone does not: its two failures concern the same constructor-default behavior as original A/B. This identifies code contribution under that fixed test set. It does not establish correct behavior outside those tests, a causal effect of the SEAL prompt, or a benefit of final verification or explicit submission.

For context, original A and B each had 6 PASS / 2 FAIL. A changed list filtering but retained the old default; B retained only diagnostic printing in production source. Original A/B full returned patches also contained scratch scripts, which are excluded from this public package. Their original patch hashes remain in the numerical provenance, not their source bodies.

## Observed trajectory, not a reconstructed success story

C executed a repository-grounded example at actual tool 10. Its output provided a semantic diagnosis of the Issue's second reported behavior despite exit status zero and no assertion. C then changed the constructor default at tool 14 and the filtering logic at tool 15. No failing check occurred between those edits. C ran no check after its last source change. A/B also discussed the default-value behavior; this was not unique knowledge of C.

All three trajectories stopped at context overflow, with zero explicit `submit_patch` calls and zero ordinary final texts. Original C's scored artifact was the Runner-returned workspace fallback patch. The case therefore does **not** demonstrate SEAL's final-verification or commitment mechanism.

## Source commitments and reproducibility

[`source_provenance.json`](source_provenance.json) identifies the original score/output hashes, the post-hoc registration and scorer source commitments, patch hashes, upstream commit, and license source. [`../data/abjad_results.json`](../data/abjad_results.json) contains only explicit public fields: outcome counts, validity/exit status, origins, timeline counts, and hashes. [`environment.json`](environment.json) records dependency versions without machine paths or endpoint information.

The original C raw score SHA256 is `211f459182e5237c07af5eda8a35ba3d83a607ea2ccefd1474b8d974e09344a5`. The public data verifier checks the patch-file hashes and recorded counts, but cannot infer the contents of withheld private sources from their digests.

Statistics reproduce offline with the repository's standard-library verifier. Rerunning the original eight-test task evaluation additionally requires the excluded qualified snapshot, dependency setup, and private scoring integration. Applying a patch manually to the public upstream source is not equivalent to recovering that frozen scoring environment.

## Licensing

Patch context modifies upstream MIT-licensed code. The exact upstream license and copyright notice are preserved in [`../LICENSES/abjad-ext-nauert.txt`](../LICENSES/abjad-ext-nauert.txt). Patch provenance does not transfer ownership of upstream code or relicense it under a manuscript/data license. The public root license scope and [`../docs/third_party_licenses.md`](../docs/third_party_licenses.md) apply separately.
