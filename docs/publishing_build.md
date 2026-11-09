# Publishing build and verification

Statistical verification uses Python 3.11+ and only its standard library. `verify_statistics.py` checks source-bound public input hashes before calculating counts. It never imports the optional PDF libraries. `render_figures.py` invokes that verifier and generates native SVG text/rectangles/lines; no raster asset or embedded font is used.

The optional PDF build was run with Python 3.12.14, ReportLab 5.1.0 and svglib 2.4.0. The two presentation dependencies are pinned in `requirements-render.txt`; dependency packages are not bundled. ReportLab and svglib retain their own licenses in their separate distributions. PDF building is not necessary to reproduce statistics. It reads only the released Markdown and local SVGs and does not retrieve external resources.

The PDF uses standard PDF Type 1 fonts (Helvetica, Times and Courier) without embedding font files. Figures remain vector objects; no private attachments, raster images, JavaScript or scoring payloads are included. The build enables ReportLab's invariant mode for deterministic output in the same publishing environment. Its fixed year-2000 PDF metadata timestamps are reproducibility metadata, **not** the date of an experiment, preregistration or publication; the visible release version is 2026-11-09.

Inspection of every rendered page, extracted PDF text, PDF links/attachments/font resources, and SVG XML was part of the release audit. The final manifest binds the actual PDF, Markdown, SVG, data, scripts, patches and notices by SHA256. Rebuilding with another dependency version may change PDF bytes without changing numerical content. The statistical outputs and SVGs can be regenerated without the PDF dependencies.

The protocol, model-service versions and original task dependencies are documented separately in [environment.md](environment.md). That historical environment is not packaged here and is not implied by installing the publishing tools.

Package metadata in the publishing environment records ReportLab 5.1.0 under its BSD license and svglib 2.4.0 under LGPL-3.0-or-later. These libraries are installed separately, not distributed as source or embedded libraries in this repository. Private release inspection additionally used pypdf 7.0.0 and pypdfium2 5.15.1; neither is a requirement of the public statistical verifier or included as a package here. No fonts from any of those installations are redistributed.
