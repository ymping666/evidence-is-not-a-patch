# Third-party material and license review

This document describes the redistributed third-party material, its verified source, and what has deliberately not been copied. It does not relicense third-party code or claim ownership of it. The root license scope for newly authored research assets is separate.

## Abjad patch context: MIT

The only redistributed upstream implementation text is the small unified-diff context in the three Abjad patches. Its source repository is [Abjad/abjad-ext-nauert](https://github.com/Abjad/abjad-ext-nauert), commit `520f389f06e21ee0a094016b4f1e2b0cb58263c1`, file `abjadext/nauert/gracehandlers.py`.

The exact `LICENSE` member was read from the same frozen source snapshot used in scoring, not inferred from today's default branch. It states **MIT License**, **Copyright (c) 2018-2020 Abjad**. The complete permission, notice and disclaimer are preserved without editing in [`../LICENSES/abjad-ext-nauert.txt`](../LICENSES/abjad-ext-nauert.txt); SHA256 `df7843f64191a5372004bafa37f97eb9f457ba0c367e8111c77c368eb96afc3c`.

MIT permits copying, modification and distribution subject to retaining the copyright and permission notice. These patches are therefore accompanied by that notice. The release does not imply that the research authors own the upstream context, or that a manuscript/data license changes its terms. The patches are identified by exact hashes and their Agent-output or later code-ablation origin, rather than falsely attributed to upstream maintainers.

## Statistics and source commitments

The public data contain derived factual observations: anonymized labels/counts, numerical losses/token totals, exit codes, exposure strata and SHA256 commitments. They do not reproduce Issue descriptions, raw model conversations, task tests or reference implementations. Anonymous stable IDs preserve statistical relationships. Original benchmark material is cited in the paper but is not redistributed as a task dataset here.

## Referenced but not redistributed

Budget-Fit V5, model weights and tokenizer files, official/private scorer code, compatibility overlays, task dependencies, complete snapshots, reference repairs, API payloads and the earlier private reviewer ZIP are excluded. Public bibliographic citations and package version names are attribution, not a copy of those packages or papers. Readers need their own lawful access and applicable licenses to obtain them elsewhere.

New SVG figures are programmatically authored diagrams made from released numerical facts and generic vector/text primitives; no third-party raster image or font file is supplied. PDF rendering dependencies and any font embedding are checked by the release-level publishing audit; this Abjad review does not assume a font license merely from its installation on a machine.

## Verification performed

The source-snapshot digest, three patch digests, original and post-hoc score/output digests, environment equality and MIT license bytes were checked by a CPU-only export smoke. Only explicit fields were selected from score records. No captured command, new scorer, model or GPU was executed. A separate release-wide allowlist and sensitivity scan must cover every final published file, including the rendered PDF, before push.
