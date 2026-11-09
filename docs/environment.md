# Recorded environment and the public runtime

## Running public statistics

The statistical verifier is standard-library Python and requires Python 3.11 or newer. It needs no GPU, Kaggle account, API token, network, model, task checkout, package installation, or private scoring service. It parses the released data and recomputes paper statistics; it does not import or execute task code or replay captured commands.

The PDF/figure generation tools, if used, are a separate optional publishing environment. Their dependencies are not requirements for statistics. No model weights, environment binaries, wheels, or third-party Python packages are bundled in this repository.

## Original P120 serving

The retained launch receipts record NVIDIA A100-SXM4-40GB devices, tensor parallel size 1, bfloat16 compute, maximum model length 32,768, maximum sequences 1, batched-token cap 8,192, chunked prefill, and GPU-memory target 0.82. Device UUIDs, process identities, private paths and serving endpoints are omitted. Receipts are summarized in [`../abjad/environment.json`](../abjad/environment.json), with original source SHA256 commitments.

| Component | Recorded version |
| --- | --- |
| Model | Unadapted Gemma-4-31B IT QAT W4A16 compressed-tensors |
| PyTorch | 2.10.0 |
| vLLM | 0.19.1 |
| Transformers | 5.13.1 |
| adk-submission | 0.2.12 |
| swegemma | 0.2.7 |

The official compatibility overlay and execution/scoring integration are identified by hashes in the provenance. They are not redistributed, and version strings alone do not reconstruct them. The public verification runtime is not a replacement for that historical environment.

## Abjad scoring and two CPU ablations

The scoring host recorded Python 3.12.14; the task sandbox uses CPython 3.9 and a frozen per-task dependency set. Key task packages are Abjad 3.3, pytest 8.3.5, quicktions 1.19, and uqbar 0.4.8. The complete recorded **version list**, without installed package source or binary files, is included in `abjad/environment.json`.

Original C and both later CPU patch ablations share these identities:

- Upstream source base commit: `520f389f06e21ee0a094016b4f1e2b0cb58263c1`.
- Official prepared baseline tree: `6041f6620d3f4b3d420e92e8f1a7883f68dc7291`.
- Task snapshot SHA256: `d7953a132fb65aa4218ce2dd0b9007fb364b335cb404f8cb2e9db2e1b73a01f6`.
- Dependency receipt SHA256: `24f911284484523afb70b898623fdc92ddb7ce98adfb3ffc26c8b6564bfba6eb`.
- Version-directory fingerprint: `d324c105319ab553`.
- Dependency contents fingerprint: `038859e0e7eb1f90ed40e8bf456f410920736a47a75cc0b372690716ccb60610`.

Both CPU variants use a 180-second scoring timeout and one configured numerical-library thread. The raw scorer's test exit codes are 0 for DEFAULT_ONLY and 1 for FILTER_ONLY; both scoring receipts are valid. The process wrapper returns 0 when scoring succeeded, even when tests fail, so wrapper exit and test exit are different fields.

These hashes document equality checks recorded at execution time. They do not supply the withheld snapshot/scorer or independently reveal their contents. Installation into a newer environment is not assumed equivalent. Historical panels before hardware migration are not pooled with P120 for timing, throughput, or efficiency claims.
