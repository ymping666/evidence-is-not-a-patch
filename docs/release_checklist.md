# Reviewed publication checklist

This checklist concerns the selected release, not the complete development repository. Reviews are assistant-assisted source, numerical and file inspections; they are not independent human annotation of the experimental corpus.

- [x] New repository and new public history; no fork, private commits, branches or Git objects.
- [x] Explicit file allowlist in `release_manifest.json`, with bytes, SHA256, classification and rights basis for each item. The manifest control file cannot contain its own digest and is separately committed.
- [x] Latest frozen manuscript is the documented parent; only public layout/captions/artifact text are adapted. Three main tables and three SVGs use frozen results.
- [x] Figure 2 and Table 1/2/3 are recomputed from minimal anonymous records, preserving repeated-task/check dependence. Abjad Figure 3 distinguishes original scores from later CPU code ablations.
- [x] Original P120 UNKNOWN is retained; a source-attributed FAIL is a separate view, not a new valid raw score.
- [x] No publication-time agent generation, training, GPU use or task scoring. Statistical recomputation is labeled as aggregation of frozen observations.
- [x] Three exact production-only Abjad patches; raw score provenance provided as whitelisted fields and source hashes, without private tests or full raw score containers.
- [x] Upstream MIT notice read from the same frozen source snapshot, preserved byte for byte, and linked beside the patches. No blanket relicensing of third-party or excluded material.
- [x] All text and structured exports scanned for credential forms, machine paths/endpoints and private repository URLs; data keys/contents inspected for excluded payloads. Public PDF text was separately extracted and inspected before its exact bytes were manifest-pinned.
- [x] No private tests, reference/gold repairs, task scorer, full source snapshot, model/environment binary, prompt bundle, API archive, old reviewer ZIP, credential or private history is included.
- [x] SVGs contain editable text/vector primitives, with no raster images, embedded font, external resource or script. Every PDF page was visually inspected; no attachments, JavaScript or embedded font file were found.
- [x] Standard-library statistics and release checks run from a clean copied release directory, without access to private data, scorer, Kaggle credentials, GPU or model.
- [x] Detailed protocols, actual recorded environments, source commitments, local-preregistration limitations and reproduction boundaries are disclosed.

Hash consistency and source commitments are useful provenance but do not independently prove hidden source content, execution or preregistration timestamps. The public script does not rerun the private task tests or reproduce every qualitative/semantic claim from raw trajectories. Anonymous public access and exact committed files are verified after publication; this document alone is not evidence of a venue submission or acceptance.
