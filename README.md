# Research Notes

Notes and experiments investigating how neural systems represent, transform, preserve, and use information.

Much of this work focuses on compact learned representations: what information survives compression, how representation geometry constrains computation, and whether information that remains present in a learned state is actually accessible to — and used by — downstream computation.

The broader goal is to develop a more precise account of representation and learned computation by separating questions that are easy to conflate: **what information is present, what information is accessible, what information is used, and what information affects behavior.** Distinguishing these cases can change both how an experimental result should be interpreted and which intervention is rational to try next.

The work combines empirical experiments, mathematical analysis, machine-checked results, and small reproducible examples. Results are presented with explicit boundaries between observation, formal result, assumption, and hypothesis.

## Start here

The notes reconstruct the research in the order the questions developed. The first milestone begins with the original representation question rather than the current experimental frontier.

1. [What if text were a signal?](notebooks/001_text_as_signal.ipynb)
2. [Where did the spectral loss occur?](notebooks/002_locating_representation_loss.ipynb)
3. [Coordinates matter; operations matter more](notebooks/003_coordinates_and_matched_operations.ipynb)
4. [Isolating the phase-aware mechanism](notebooks/004_isolating_phase_attention.ipynb)
5. [The unit-hypersphere anomaly](notebooks/005_unit_hypersphere_anomaly.ipynb)
6. [A dramatic endpoint can still mislead](notebooks/006_endpoint_can_mislead.ipynb)
7. [Derive before training](notebooks/007_derive_before_training.ipynb)
8. [What does the sphere actually do?](notebooks/008_frozen_mechanism_tests.ipynb)
9. [From hypothesis sprawl to a theorem ledger](notebooks/009_theorem_ledger_method.ipynb)
10. [What state should a reasoner preserve?](notebooks/010_dynamic_quotient.ipynb)
11. [Geometry should follow invariance, not aesthetics](notebooks/011_geometry_from_invariance.ipynb)
12. [Natural-source task distinctions](notebooks/012_natural_source_distinctions.ipynb)
13. [Accessible does not imply used](notebooks/013_accessible_not_used.ipynb)

The reconstruction plan, historical anchors, disclosure decisions, and future milestone slot are recorded in [`CHRONOLOGY.md`](CHRONOLOGY.md).

## Two complementary ways to read

**Milestone path — learn through the research.** Read notebooks in order. Each begins with a scientific question, develops only the machinery needed to investigate it, includes runnable examples, and ends with understanding questions. Reconstructed notes label the historical research period separately from their public reconstruction date.

**Reference path — follow concepts as needed.** The [`reference/`](reference/) material provides reusable definitions, mathematical foundations, methods, formal checkpoints, and a concept index. Notebook sticky notes give the local explanation; linked reference pages provide the deeper treatment.

## Educational conventions

### Sticky notes

A sticky note is a short, deliberately repeated reminder embedded where a concept is actually being used.

> **Sticky note — affine:** An affine map is a linear transformation plus a bias: `z = Wx + b`. It can rotate, rescale, mix, and shift coordinates, but it cannot create nonlinear feature interactions by itself. [Deeper reference →](reference/glossary.md#affine-map)

Repetition is intentional: the goal is to learn concepts through repeated use rather than isolated memorization.

### Understanding questions

Each milestone ends with short questions that check whether the argument can be reconstructed, rather than whether terminology has been memorized.

### Formal checkpoints and epistemic markers

Where mathematics can be separated cleanly from empirical interpretation, the notes link to the public [`theorem-library`](https://github.com/pH34r-pH/theorem-library) rather than copying Lean proofs here.

- **✓ Formal checkpoint** — the linked mathematical statement has a public Lean proof.
- **● Observation** — an experimental measurement under a stated protocol.
- **◇ Assumption** — a premise not established by the present evidence.
- **? Hypothesis** — a proposed explanation still open to testing.

A formal checkpoint applies only to the encoded theorem and its assumptions. It does not automatically promote surrounding scientific interpretation to theorem status. [How the formal layer works →](reference/formal-methods/index.md)

### Result boundaries

Every milestone explicitly states **What this does not show**. A central goal of this project is learning to distinguish an observation from the stronger interpretations it may suggest.

## Reference map

- [Concept index](reference/index.md)
- [Glossary](reference/glossary.md)
- [Experimental reasoning](reference/experimental-reasoning.md)
- [Representation and readout](reference/representation-and-readout.md)
- [Formal methods and claim boundaries](reference/formal-methods/index.md)
- [Public formal checkpoints](reference/formal-methods/checkpoints.md)
- [Public Lean theorem library](https://github.com/pH34r-pH/theorem-library)
- [Editorial and disclosure guide](notes/EDITORIAL_GUIDE.md)

## Source-of-truth boundaries

`research-notes` is an educational presentation layer, not the authoritative theorem ledger.

The public `theorem-library` owns public Lean source and intrinsic proof/build validation. The private research laboratory owns theorem-ledger lifecycle state, scientific correspondence, provenance, active experiments, and unpublished interpretation. Stable theorem identifiers let these layers refer to the same formal object without duplicating ledger state.

## Disclosure policy

**Public:** stable research questions; high-level methods; selected validated outcomes; synthetic reproductions of concepts; reusable public mathematical proofs; mathematical and methodological background; interpretation boundaries.

**Private:** active experiment branches; exact private datasets/checkpoints; theorem-ledger research state; unfinished hypotheses; private negative-result chronology where it exposes the active frontier; and end-to-end details that would reproduce ongoing unpublished work.

## Status

Independent research, ongoing.
