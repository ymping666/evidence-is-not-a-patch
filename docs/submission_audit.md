# Gemma 4 Developer Agent Paper Track: submission audit

Audit date: **2026-11-09**. This checklist is for the public manuscript in [`paper/paper.pdf`](../paper/paper.pdf), not a declaration that a Kaggle Writeup has been submitted.

## Official requirements

Primary source: [Google — The Gemma 4 Developer Agent Paper Track: Submission Requirements](https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/overview/submission-requirements). Consult the live rule page again immediately before pressing Submit.

| Item | Official track requirement | Public manuscript status |
| --- | --- | --- |
| Deadline | 2026-11-12, 23:59 UTC | Prepare Writeup and submit before the deadline; upload alone is not submission. |
| Length | Up to 3,000 words | See `paper/build_receipt.json`; conservatively counts references, figure text, headers, footers, and page numbers. |
| Required sections | Title, subtitle, abstract, introduction, research methods and experiments, related works and citations | Present in the PDF; named sections combine methods and results. |
| Format | Kaggle Writeup; optional arXiv-ready PDF through a public Project Link | Public GitHub PDF link available; no official ICLR/NeurIPS/ICML template is imposed. |
| Review criteria | Novelty, Quality, Relevance, Verifiability, Clarity: 20% each | Source-bound delivery audit and replay protocol; limits and evidence access disclosed. |
| Publication status | Original work, non-archival competition track | No claim of prior venue publication or acceptance. |

## Citations and bibliography

- Ten consecutively numbered references `[1]`–`[10]` are used consistently between the manuscript and `references.bib`.
- Research statements cite first-party papers or their archived preprints; arXiv-only 2026 work remains labeled as **arXiv preprint**, not a published conference paper.
- SWE-bench is identified with its ICLR 2024 proceedings record, not only the 2023 preprint: [ICLR record](https://openreview.net/forum?id=VTF8yNQM66).
- SWE-Gym is identified with its ICML 2025 proceedings volume and pages: [PMLR 267](https://proceedings.mlr.press/v267/pan25g.html).
- The target track does not mandate a single bibliography style; numbered academic citations are acceptable as long as bibliographic metadata is accurate and consistent.

## Claim-strength checks

| Central observation | Evidence in paper | Inference limit |
| --- | --- | --- |
| Local checks can target a different source from the eventual patch | 213/549 reconstructed check-source states differ from the final artifact; 15/161 last-check states also differ | A mismatch is source drift, not proof that earlier checks were useless. |
| Zero-exit checks can fail to discriminate correct and incorrect candidates | 314 qualified three-state triplets; all-three-zero among failing-candidate/zero-exit units: 16/16, 14/19, 16/21, and 36/36 | Selected checks/environments; stdout and exception content can still carry useful information; not all historical checks. |
| Local improvement is not equivalent to complete-agent repair improvement | SFT validation NLL falls by 31.5%, while recorded repairs change from 12/24 to 11/24 | Small, overlapping development panels; not a causal or held-out population effect. |
| Prompt-only delivery guidance remains exploratory | SEAL original 72 runs: A 5/24, B 5/24, C 6/24; original UNKNOWN preserved | One reused-DEV success flip; no reliable prompt effect or fresh-task generalization. |
| Abjad isolates code contributions to an eight-test outcome | Original C 8/8, later CPU default-only 8/8, filtering-only 6/8 | Different execution origins, tests incomplete; not proof of prompt causality, explicit submission, or full repair correctness. |

## Last-mile manual actions

1. Create or update the Kaggle Writeup with the title, subtitle, abstract, methods/experiments, related work and citations matching the released PDF.
2. Include a **publicly accessible** Project Link to the exact released PDF, not to a private development repository.
3. Recheck the live rule page for changed instructions, inspect the rendered Writeup, and click **Submit** before the deadline. Saving a draft is not submission.
4. Keep the description honest about missing private scorer/tests and the scope of offline statistical recomputation.
