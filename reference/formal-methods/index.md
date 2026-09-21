# Formal methods

Some questions in this research depend on trained models and have to be answered experimentally. Others reduce to mathematical claims that can be settled before another model is trained.

I use formal methods for the second category, especially when a plausible but incorrect mathematical intuition could motivate an entire branch of experiments. The goal isn't to formalize the research end to end; it's to establish exact boundaries around the parts that mathematics can decide.

## Example: what normalization actually does

For a nonzero vector,

`N(x) = x / ||x||`

has derivative

`DN_x = (1 / ||x||)(I - uuᵀ)`

where `u = x / ||x||`.

This gives an exact radial/tangent distinction: infinitesimal changes in magnitude disappear under normalization, while tangent changes survive with gain `1 / ||x||`.

> ✓ **Formal checkpoint — LIB-SPH-002 / FRM-000020**  
> [Plain-language checkpoint →](checkpoints.md#lib-sph-002--frm-000020--normalization-derivative-anisotropy) · [Lean source →](https://github.com/pH34r-pH/theorem-library/blob/main/TheoremLibrary/Geometry/Sphere/Anisotropy.lean)

The boundary is just as important as the result. This theorem says how normalization acts on perturbations; it doesn't say that radial variation is useless, that tangent variation represents semantics, or that normalization will improve a trained model. Those require empirical evidence.

## What gets formalized

Formalization is most useful when it can change the research plan. A proof or counterexample can:

- establish a property an experiment would otherwise be trying to rediscover;
- show that a proposed mechanism is mathematically impossible as stated;
- expose an assumption that needs empirical validation;
- distinguish a local result from a stronger claim about recurrent dynamics;
- eliminate an experiment that cannot distinguish the hypotheses it was intended to test.

The public [Theorem Library](https://github.com/pH34r-pH/theorem-library) contains the reusable Lean results that have been promoted out of the research program. This repository explains how those results affect the research questions.

## Reading a formal checkpoint

A formal checkpoint has three parts:

**Statement:** what was actually proved, under its stated assumptions.

**Research use:** why that mathematical fact matters to the question being investigated.

**Boundary:** what tempting stronger conclusion does *not* follow from the proof.

The Lean source is linked for readers who want to inspect the exact theorem or verify it independently. Understanding the notebook shouldn't require reading Lean.

## Evidence types

I keep mathematical and empirical evidence separate:

- **✓ Formal checkpoint** — established mathematically under explicit assumptions.
- **● Observation** — measured under an experimental protocol.
- **◇ Assumption** — required by the current argument but not established there.
- **? Hypothesis** — still open to testing.

A research argument can contain all four. The marker prevents one kind of evidence from quietly inheriting the strength of another.

## Public proofs

The [formal checkpoint index](checkpoints.md) maps the mathematical results used in these notes to their public Lean sources.

The [Theorem Library](https://github.com/pH34r-pH/theorem-library) is the public machine-checkable source for those proofs.
