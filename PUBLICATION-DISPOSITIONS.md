# Public research publication dispositions

This map defines the reader-facing role of every source notebook and reference page in the public Research Notes collection. Canonical articles carry the reviewed narrative; notebooks remain unchanged as chronological and computational source records.

## Chronological notebooks

| Source record | Disposition | Canonical reader page |
| --- | --- | --- |
| [Milestone 001](notebooks/001_text_as_signal.ipynb) | canonical article | [Milestone 001 — What if text were a signal?](articles/001-text-as-signal.md) |
| [Milestone 002](notebooks/002_locating_representation_loss.ipynb) | canonical article | [Milestone 002 — Where did the spectral loss occur?](articles/002-locating-representation-loss.md) |
| [Milestone 003](notebooks/003_coordinates_and_matched_operations.ipynb) | canonical article | [Milestone 003 — Coordinates matter; operations matter more](articles/003-coordinates-and-matched-operations.md) |
| [Milestone 004](notebooks/004_isolating_phase_attention.ipynb) | canonical article | [Milestone 004 — Isolating the phase-aware mechanism](articles/004-isolating-phase-attention.md) |
| [Milestone 005](notebooks/005_unit_hypersphere_anomaly.ipynb) | canonical article | [Milestone 005 — The unit-hypersphere anomaly](articles/005-unit-hypersphere-anomaly.md) |
| [Milestone 006](notebooks/006_endpoint_can_mislead.ipynb) | canonical article | [Milestone 006 — A dramatic endpoint can still mislead](articles/006-endpoint-can-mislead.md) |
| [Milestone 007](notebooks/007_derive_before_training.ipynb) | canonical article | [Milestone 007 — Derive before training](articles/007-derive-before-training.md) |
| [Milestone 008](notebooks/008_frozen_mechanism_tests.ipynb) | canonical article | [Milestone 008 — What does the sphere actually do?](articles/008-frozen-mechanism-tests.md) |
| [Milestone 009](notebooks/009_theorem_ledger_method.ipynb) | canonical article | [Milestone 009 — From hypothesis sprawl to a theorem ledger](articles/009-theorem-ledger-method.md) |
| [Milestone 010](notebooks/010_dynamic_quotient.ipynb) | canonical article | [Milestone 010 — What state should a reasoner preserve?](articles/010-dynamic-quotient.md) |
| [Milestone 011](notebooks/011_geometry_from_invariance.ipynb) | canonical article | [Milestone 011 — Geometry should follow invariance, not aesthetics](articles/011-geometry-from-invariance.md) |
| [Milestone 012](notebooks/012_natural_source_distinctions.ipynb) | canonical article | [Milestone 012 — Natural-source task distinctions](articles/012-natural-source-distinctions.md) |
| [Milestone 013](notebooks/013_accessible_not_used.ipynb) | canonical article | [Milestone 013 — Accessible does not imply used](articles/accessible-does-not-imply-used.md) |
| [Visual Intuition Atlas](notebooks/visual_intuition_atlas.ipynb) | supporting/source notebook | The original demonstrations remain as source. Their explanatory material is embedded in the relevant articles below. |

The Atlas-to-article crosswalk preserves its eight original topics without keeping a separate primary-reader destination:

1. Fourier signal and frequency coordinates → [Milestone 001](articles/001-text-as-signal.md).
2. Phase-aware similarity → [Milestone 004](articles/004-isolating-phase-attention.md).
3. Endpoint and checkpoint selection → [Milestone 006](articles/006-endpoint-can-mislead.md).
4. Normalization's radial/tangent derivative → [Milestone 007](articles/007-derive-before-training.md).
5. Finite-horizon Jacobian products → [Milestone 008](articles/008-frozen-mechanism-tests.md).
6. Radius/angle coupling → [Milestone 011](articles/011-geometry-from-invariance.md).
7. Natural-source context support → [Milestone 012](articles/012-natural-source-distinctions.md).
8. Probe recoverability versus native use → [Milestone 013](articles/accessible-does-not-imply-used.md).

The phase/coordinate experiment in [Milestone 003](articles/003-coordinates-and-matched-operations.md), the stage-localization narrative in [Milestone 002](articles/002-locating-representation-loss.md), and the method/theory narratives in [Milestones 009](articles/009-theorem-ledger-method.md) and [010](articles/010-dynamic-quotient.md) remain separate because combining them would blur distinct questions and chronology.

## Reusable reference and formal sources

| Public source | Disposition | Role |
| --- | --- | --- |
| [Concept index](reference/index.md) | methodology/reference | Navigation among shared definitions, methods and formal material. |
| [Representation and readout](reference/representation-and-readout.md) | methodology/reference | Definitions for information, access, use and causal function. |
| [Experimental reasoning](reference/experimental-reasoning.md) | methodology/reference | Controls, evaluation and bounded negative results. |
| [Glossary](reference/glossary.md) | methodology/reference | Reusable terms and stable anchors. |
| [Formal methods index](reference/formal-methods/index.md) | methodology/reference | Scope and boundaries of theorem-supported claims. |
| [Formal methods README](reference/formal-methods/README.md) | methodology/reference | Entry point and source notes for the public formal-methods material. |
| [Formal checkpoint list](reference/formal-methods/checkpoints.md) | methodology/reference | Stable theorem identifiers and their assumptions. |
| [Theorem Library](https://github.com/pH34r-pH/theorem-library) | authoritative formal source | Machine-checked proofs remain owned by the theorem repository and are linked from the relevant articles. |

The directory `notes/` contains workflow and planning documentation; it is not part of the public article/notebook input set.
