# Research Notes

Notes and experiments investigating how neural systems represent, transform, preserve, and use information.

Much of this work focuses on compact learned representations: what information survives compression, how representation geometry constrains computation, and whether information that remains present in a learned state is actually accessible to — and used by — downstream computation.

The broader goal is to develop a more precise account of representation and learned computation by separating questions that are easy to conflate: **what information is present, what information is accessible, what information is used, and what information affects behavior.** Distinguishing these cases can change both how an experimental result should be interpreted and which intervention is rational to try next.

The work combines empirical experiments, mathematical analysis, machine-checked results, and small reproducible examples. Results are presented with explicit boundaries between observation, formal result, assumption, and hypothesis.

## Start here

### Milestone 001 — Accessible does not imply used

The current research thread asks:

> When a compact neural state appears to lose task performance, did the representation actually destroy the relevant information, or is the downstream consumer merely failing to use information that remains accessible?

The first notebook develops this distinction using a runnable synthetic affine-softmax probe and explains why probe success is evidence of **accessibility**, not automatically evidence of **causal use**.

- [`notebooks/001_accessible_not_used.ipynb`](notebooks/001_accessible_not_used.ipynb)

## Two complementary ways to read

**Milestone path — learn through the research.** Read notebooks in order. Each begins with a scientific question, develops only the machinery needed to investigate it, includes runnable examples, and ends with understanding questions.

**Reference path — follow concepts as needed.** The [`reference/`](reference/) material provides reusable definitions, mathematical foundations, methods, formal checkpoints, and a concept index. Notebook sticky notes give the local explanation; linked reference pages provide the deeper treatment.

## Educational conventions

### Sticky notes

A sticky note is a short, deliberately repeated reminder embedded where a concept is actually being used.

> **Sticky note — affine:** An affine map is a linear transformation plus a bias: `z = Wx + b`. It can rotate, rescale, mix, and shift coordinates, but it cannot create nonlinear feature interactions by itself. [Deeper reference →](reference/glossary.md#affine-map)

Repetition is intentional: the goal is to learn concepts through repeated use rather than isolated memorization.

### Understanding questions

Each milestone ends with short questions that check whether the argument can be reconstructed, rather than whether terminology has been memorized.

Examples:

- Why use an affine probe before a nonlinear probe?
- Why doesn't a successful probe prove that the native model uses the information?
- What does freezing the representation rule out?
- What result would change the next experimental target?

### Formal checkpoints and epistemic markers

Where mathematics can be separated cleanly from empirical interpretation, the notes link to the public [`theorem-library`](https://github.com/pH34r-pH/theorem-library) rather than copying Lean proofs here.

Four markers help make the evidence type explicit:

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
