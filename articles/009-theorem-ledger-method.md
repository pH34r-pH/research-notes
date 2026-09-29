---
title: "Milestone 009 — From hypothesis sprawl to a theorem ledger"
description: "How can checked mathematics constrain the next architecture experiment?"
short_title: "From hypothesis sprawl to a theorem ledger"
date: 2026-09-29
authors:
  - name: Tyler J.H.G.
tags:
  - research milestone
  - executable article
---

(milestone-009)=
# Milestone 009 — From hypothesis sprawl to a theorem ledger
**Research period:** September 3, 2026 onward  
**Historical anchors:** #196, #198–#200, later #257

The hypersphere work opened a much larger design space. If direction could matter independently from magnitude, should hierarchy use hyperbolic geometry? Could a concept be represented by a subspace instead of a vector? Should relationships be transformations rather than coordinates? Would product spaces, graph structure, or sheaf-like transport preserve distinctions that ordinary vector representations collapse?

Each idea was plausible enough to turn into an experiment. That was exactly the problem.

Building all of them would have converted mathematical uncertainty into architecture search: implement a model, train it, measure the result, then try to infer whether the underlying idea had ever made sense in the first place. I wanted to reverse that order.

The theorem ledger grew out of a simpler rule: **before testing whether an architecture works, ask what can already be proved about the claim that motivates it.**

(009-theorem-ledger-method-visual-intuition)=
## Visual intuition
```{figure} ./009_theorem_ledger_method.svg
:label: 009-theorem-ledger-method-intuition
:alt: Four epistemic labels distinguish formal results, empirical observations, assumptions and open hypotheses.

Four labels distinguish the kinds of support a claim has.
```

## Four kinds of evidence

The research started separating claims by the kind of evidence supporting them:

- ✓ **Formal checkpoint** — a mathematical statement established under explicit assumptions.
- ● **Observation** — something measured under a specified empirical protocol.
- ◇ **Assumption** — a premise the argument currently depends on without establishing it.
- ? **Hypothesis** — an explanation or prediction that remains open to testing.

These categories prevent several easy mistakes. An observation can motivate a theorem without proving it. A theorem can constrain an experiment without predicting its result. An assumption can be useful without quietly becoming a fact, and a hypothesis can survive several experiments without becoming mathematically necessary.

For example:

`normalization removes infinitesimal radial perturbations → formal checkpoint`

`the unit model had lower loss at the #164 endpoint → observation`

`radial variation is nuisance information → hypothesis`

Those statements are related, but they aren't interchangeable.

## The ledger

The ledger records the relationships between claims: what each statement assumes, what supports it, what it rules out, what remains unresolved, and which proposed experiments depend on it.

That last part made the system practically useful. A proof can sometimes eliminate an experiment entirely. A counterexample can kill a proposed universal architecture claim. A theorem may also narrow an experiment from “does this whole architecture work?” to one empirical premise that mathematics can't settle.

The public [Theorem Library](https://github.com/pH34r-pH/theorem-library) contains the reusable formal mathematics that emerged from this process, including machine-checked Lean proofs where appropriate. The ledger itself serves a different purpose: it tracks how mathematical results change the research program.

> **Sticky note — counterexample:** a single valid case that violates a universal claim is enough to prove that the claim, as stated, is false. This makes counterexamples especially useful for pruning broad architecture hypotheses before implementation.

## Try a small example

A small dictionary labels three claims by the evidence supporting them. The saved output below is available without starting Python.

```{code-cell} python
:label: 009-theorem-ledger-method-teaching-example
:tags: [illustrative, thebe]

claims = {
    'normalization radial derivative is zero': 'formal',
    'unit model had lower NLL at #164 endpoint': 'observation',
    'radial direction is nuisance': 'hypothesis',
}
for claim, kind in claims.items(): print(f'{kind:11s} | {claim}')
```

**Saved output:**

```text
formal      | normalization radial derivative is zero
observation | unit model had lower NLL at #164 endpoint
hypothesis  | radial direction is nuisance
```


## Research context

This approach wasn't based on the idea that machine learning can be reduced to theorem proving. It came from the opposite observation: the project was mixing questions that require experiments with questions that mathematics could already answer.

As I compared the growing design space with existing work in geometric deep learning, information theory, dynamical systems, representation learning, and formal methods, many apparently novel architecture questions turned out to contain established mathematical subproblems. In other cases, a short derivation or counterexample was enough to expose a missing assumption.

The useful role of the literature was therefore broader than supplying architectures to reproduce. Existing theory could tell me which parts of an idea were already understood, which claims were too strong, and where an empirical question actually began.

## Interpretation

A proof establishes its encoded conclusion under its assumptions. Connecting those assumptions to a trained model or dataset requires empirical evidence.

The ledger made that connection explicit. It kept mathematical results, observations, assumptions, and hypotheses in their proper roles, so proofs and counterexamples could eliminate impossible or redundant branches before training.

(009-theorem-ledger-method-sources)=
## Sources and chronology
- [Milestone notebook 009 — preserved chronological source](../notebooks/009_theorem_ledger_method.ipynb)
- [Research chronology](../CHRONOLOGY.md)
- [Publication dispositions and Atlas-to-article map](../PUBLICATION-DISPOSITIONS.md)

The matching Atlas theme is **Claim-type distinctions**. The original [Visual Intuition Atlas notebook](../notebooks/visual_intuition_atlas.ipynb) remains available as a source record; this article carries the relevant static explanation inline.

The next chronological article is [**Milestone 010 — What state should a reasoner preserve?**](./010-dynamic-quotient.md).
