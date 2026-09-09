# Research Notes

A public, educational research notebook on compact neural representations, representation geometry, information accessibility, and downstream utilization.

This repository is organized more like a **living textbook and research blog** than a conventional source repository. Milestone notebooks tell the chronological research story with runnable examples; the reference material supplies reusable definitions, mathematical background, and conceptual links.

The active experimental laboratory is intentionally separate and private. This repository contains stable questions, methods, selected validated outcomes, synthetic demonstrations, and carefully bounded interpretations.

## Start here

### Milestone 001 — Accessible does not imply used

The current research thread asks:

> When a compact neural state appears to lose task performance, did the representation actually destroy the relevant information, or is the downstream consumer merely failing to use information that remains accessible?

The first notebook develops this distinction using a runnable synthetic affine-softmax probe and explains why probe success is evidence of **accessibility**, not automatically evidence of **causal use**.

- [`notebooks/001_accessible_not_used.ipynb`](notebooks/001_accessible_not_used.ipynb)

## Two complementary ways to read

**Milestone path — learn through the research.** Read notebooks in order. Each begins with a scientific question, develops only the machinery needed to investigate it, includes runnable examples, and ends with understanding questions.

**Reference path — follow concepts as needed.** The [`reference/`](reference/) material acts like the back matter of a textbook: definitions, mathematical foundations, methods, and a concept index. Notebook sticky notes give the local explanation; linked reference pages provide the deeper treatment.

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

### Result boundaries

Every milestone explicitly states **What this does not show**. A central goal of this project is learning to distinguish an observation from the stronger interpretations it may suggest.

## Reference map

- [Concept index](reference/index.md)
- [Glossary](reference/glossary.md)
- [Experimental reasoning](reference/experimental-reasoning.md)
- [Representation and readout](reference/representation-and-readout.md)
- [Editorial and disclosure guide](notes/EDITORIAL_GUIDE.md)

## Disclosure policy

**Public:** stable research questions; high-level methods; selected validated outcomes; synthetic reproductions of concepts; mathematical and methodological background; interpretation boundaries.

**Private:** active experiment branches; exact private datasets/checkpoints; unfinished hypotheses; private negative-result chronology where it exposes the active frontier; and end-to-end details that would reproduce ongoing unpublished work.

## Status

Independent research, ongoing.
