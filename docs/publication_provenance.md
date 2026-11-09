# Public-edition provenance

The public manuscript derives from the frozen latest integrated research draft, SHA256:

`16b1f3841d8043a755553837e3463db44dacb198207d7767e1c6138635fd9c04`

Only presentation and artifact-availability changes were made for this repository:

1. Add the conceptual repair-chain map as Figure 1.
2. Rename the existing mechanical subset diagram to Figure 2 and regenerate it from released event projections.
3. Add the source-bound Abjad trajectory/patch-ablation diagram as Figure 3.
4. Fold the old Table 4 temporal subset into the last column of Table 3. Its event-weighted denominator remains separate from unit-weighted columns.
5. Replace the obsolete private-artifact availability paragraph with the scope of this public, selected release.
6. Link the public artifact directly in the manuscript and condense two Figure 1 labels for legibility.
7. Keep the three tables intact with their captions and embed properly licensed DejaVu font subsets to avoid PDF font-substitution errors. These are layout and publishing changes only.

All original numerical outcomes, UNKNOWN labels and separate source-adjudication decisions remain unchanged. Original and later CPU scoring are distinguished in both the data and manuscript. No model or task scorer was invoked to produce this release.

Source commitments for the numerical exports are in [data/provenance.json](../data/provenance.json); the Abjad patch, score and environment commitments are in [abjad/source_provenance.json](../abjad/source_provenance.json). Logical source labels and SHA256 values replace machine paths. The private extraction mapping is deliberately not published. Hashes of withheld files do not make those files available or establish their contents to an outside reader.

The repository starts with its own new public history. No private branches, commits, Git objects, workspaces, full archives, task tests or scorer implementations are imported. This release is a scoped research export, not a reproduction of the entire development environment.

`paper/build_receipt.json` records the exact released Markdown/PDF hashes and counting conventions. Markdown contains 2,811 whitespace-separated words (2,886 lexical words), including captions, tables and references. Extracted PDF text contains 2,866 whitespace-separated words (2,977 lexical words), including figure text, repeated headers/footers, page numbers and references. Lexical counting uses `[A-Za-z0-9]+(?:[-_'][A-Za-z0-9]+)*` on the plain text; no reference or footer exemption is needed. Layout-only figure wording was condensed without changing any result.
