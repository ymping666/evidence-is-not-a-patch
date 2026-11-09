# Evidence Is Not a Patch

Research artifact for **From Local Improvement to Verified Repair: A Cross-Intervention Delivery Audit**.

This is a deliberately selected public release, built in a new repository. It is not a fork or copy of the private development repository, and contains none of its Git history.

## Paper and figures

- [Paper PDF](paper/paper.pdf) · [Markdown](paper/paper.md) · [References](paper/references.bib)
- [Figure 1: repair-chain audit map](paper/figures/figure1_repair_chain.svg)
- [Figure 2: mechanical delivery subsets](paper/figures/figure2_delivery_subsets.svg)
- [Figure 3: Abjad diagnosis and code ablations](paper/figures/figure3_abjad_ablation.svg)

All three SVGs retain editable text and vector shapes. Table 3 includes both the unit-weighted three-state matrix and the separately event-weighted post-last-change stratum. The public edition adapts layout and artifact-availability text from the frozen latest manuscript; numerical results are unchanged. See [publication provenance](docs/publication_provenance.md).

## Recompute the statistics

Python **3.11 or newer**, standard library only:

```bash
python3 -B scripts/verify_statistics.py --output /tmp/paper_statistics.json
python3 -B scripts/check_release.py
```

The first command verifies the released input hashes and recomputes Table 1/2/3, Figure 2, P120 original and separately adjudicated paired outcomes, the 2/22 exposure strata, and Abjad Figure 3 values. The second checks the release manifest, file hashes, SVG editability, exclusion rules and sensitive-information patterns. Neither command contacts a network, requires an account, imports task code, executes captured commands, or calls a scoring service.

The export contains 180 anonymized historical episodes, 716 necessary source-change/check events representing a frozen 2,451-event corpus, 314 check units with 408 historical mappings, and 72 original P120 cells. Stable anonymous IDs preserve shared-task and repeated-check relationships. These are not independent samples. [Data dictionary](docs/data_dictionary.md) · [Protocol](docs/protocol.md) · [Environment](docs/environment.md).

The small supplementary export also sums the published state-alignment panel counts and preserves source-bound E2/E3/semantic-review aggregates. It does not reconstruct raw cases or reproduce every descriptive protocol number from underlying task executions.

## Abjad case and boundaries

The [Abjad package](abjad/README.md) contains three narrow MIT-source patches: the exact original C production patch, DEFAULT_ONLY, and FILTER_ONLY. Original C passed eight tests during the 72-generation campaign. Two **later CPU patch ablations** yielded 8/8 PASS and 6 PASS/2 FAIL respectively. Their sanitized receipts and original-source hashes are separate. Current statistical recomputation adds **zero agent generations and zero scoring executions**.

The default change alone suffices for those eight tests. This does not establish prompt causality, full behavior correctness, or effective final verification: C performed no post-edit check and never explicitly submitted. P120's original UNKNOWN is preserved; the later source-attributed FAIL appears only in a separate adjudication view. SEAL remains exploratory, with one reused-DEV success flip. Human signatures remain zero; targeted assistant inspection is not full semantic review of all 72 runs.

Private tests, the task scorer, reference/gold repairs, full snapshots, prompt bundles, weights, raw trajectories/API archives, private reviewer archives, credentials and private Git history are **not included**. Source hashes identify withheld inputs but do not supply their contents or independently prove execution. See [reproduction boundaries](docs/reproduction_boundaries.md).

## Optional presentation build

```bash
python3 -B scripts/render_figures.py
python3 -m venv .venv-render
.venv-render/bin/python -m pip install -r requirements-render.txt
.venv-render/bin/python -B scripts/build_pdf.py
```

Figure generation itself is standard-library only. PDF rendering is optional and separate from statistical verification; it uses ReportLab, svglib and DejaVu fonts for embedded cross-platform typography. See [publishing build notes](docs/publishing_build.md).

## Release and rights

[Release manifest](release_manifest.json) · [Release checklist](docs/release_checklist.md) · [Third-party notices](docs/third_party_licenses.md) · [Rights scope](RIGHTS.md).

This is a public research artifact, not a claim of venue submission, acceptance, hidden-benchmark improvement, or generalization to fresh heldout tasks. The original experimental outputs remain frozen; offline export and recomputation are not new agent experiments.
