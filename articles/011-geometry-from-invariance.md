---
title: "Milestone 011 — Geometry should follow invariance, not aesthetics"
description: "Which geometry preserves the invariances a task actually needs?"
short_title: "Geometry should follow invariance, not aesthetics"
date: 2026-09-29
authors:
  - name: Tyler J.H.G.
tags:
  - research milestone
  - executable article
---

(milestone-011)=
# Milestone 011 — Geometry should follow invariance, not aesthetics
**Research period:** September 2–3, 2026  
**Historical anchors:** #194–#198

For a short period, the geometric branch of the project had an appealing working slogan: **“spheres all the way down.”** If hyperspherical state helped in one part of the model, perhaps representation, reasoning, hierarchy, relationships, and even network structure should all inherit compatible spherical geometry.

It was a useful intuition and a bad design rule.

Once I started writing down what different parts of the system were supposed to preserve, there was no reason to expect one geometry to satisfy all of them. Semantic identity, hierarchical growth, scalar quantities, relational transformations, and contextual ambiguity impose different mathematical requirements.

The question therefore changed from “which geometry should the model use?” to **“what properties does this part of the model require, and which geometries satisfy them?”**

(011-geometry-from-invariance-visual-intuition)=
## Visual intuition
```{figure} ./011_geometry_from_invariance.svg
:label: 011-geometry-from-invariance-intuition
:alt: At fixed angle, ordinary inner product changes when either vector radius changes.

At a fixed angle, changing either radius changes the inner product.
```

## A simple example: radius and direction

One proposal was to let direction represent semantic identity while radius independently represented something structural, such as argument depth or scope.

Write a nonzero vector as

`x = r u`, with `||u|| = 1`

where `u` gives direction and `r` gives magnitude.

At first this looks like two convenient channels living inside one vector. Ordinary Euclidean geometry couples them, though. In polar form its distance element is

`ds² = dr² + r² dΩ²`

so changing radius changes the scale of angular distances. Ordinary inner-product similarity has the same problem:

`q · k = r_q r_k cos(theta)`

The similarity attributed to the angle is multiplied by both magnitudes.

That means “direction carries semantics while radius independently carries structure” isn't automatically true just because we assign those interpretations to the coordinates. If the two quantities are supposed to vary independently under the model's metric and operations, a product representation or explicit side channel is a cleaner construction. If interaction between them is intentional, then a coupled or warped geometry may be exactly what we want.

> **Sticky note — product geometry:** when a state contains two factors that should vary independently, a product space keeps a separate geometry for each factor. This makes the independence an explicit property of the construction rather than something we hope emerges from coordinates that are already coupled.

## The same test applied elsewhere

The radius example became one instance of a broader pruning strategy.

**Hyperbolic geometry** is attractive for hierarchy because hyperbolic space has room for quantities that grow exponentially with distance from the center. That makes it a natural candidate when the representation really needs to preserve tree-like growth and separation. It doesn't mean that every hierarchy requires hyperbolic geometry; finite trees can also be represented in ordinary spaces under different dimensional and distortion tradeoffs.

**Subspace-valued representations** became interesting when one vector seemed too restrictive for a concept with several persistent contextual realizations. Grassmann geometry provides a natural way to represent a subspace without caring which particular basis vectors happen to describe it. That only buys something if the downstream system actually needs the subspace and is invariant to its choice of basis; if the model ultimately consumes one emitted vector, the hidden subspace may amount to a more complicated vector parameterization.

**Relation operators** produced another hard boundary. If semantic operations are order-sensitive, a family of transformations that always commute cannot represent all of them. Applying relation A and then B must sometimes differ from applying B and then A, so the operator family has to be expressive enough to preserve that distinction.

These weren't arguments for three new architectures. They were conditions an architecture would have to satisfy before an experiment became worth running.

## Research context

This pruning pass converged with several existing research areas.

Hyperbolic representation learning had already developed the connection between negative curvature and hierarchical or tree-like structure. Grassmann and other subspace methods provided established machinery for representing objects whose identity is a subspace rather than a particular coordinate basis. Geometric deep learning more broadly treats symmetry and invariance as clues about which mathematical structure a model should respect.

The literature was useful here because it turned vague geometric intuitions into sharper questions. Instead of borrowing a geometry because another model had used it successfully, I could ask what property made that geometry appropriate there and whether my problem had the same property.

That changed the role of prior work in the project. A paper using hyperbolic embeddings wasn't evidence that I should use hyperbolic embeddings; it was evidence about the conditions under which hyperbolic structure had been useful, plus a source of mathematical tools for testing whether those conditions applied here.

## Try a small example

A toy calculation holds the angle fixed and varies the radii to show how scale changes the inner product. The saved output below is available without starting Python.

```{code-cell} python
:label: 011-geometry-from-invariance-teaching-example
:tags: [illustrative, thebe]

import numpy as np
theta=np.pi/3
for rq,rk in [(1,1),(2,1),(2,3)]:
    print(rq,rk,'dot-like similarity=',rq*rk*np.cos(theta))
```

**Saved output:**

```text
1 1 dot-like similarity= 0.5000000000000001
2 1 dot-like similarity= 1.0000000000000002
2 3 dot-like similarity= 3.000000000000001
```


## Interpretation

Different parts of a system can require different invariances, growth laws, and operations, and therefore different geometries. Mathematical compatibility makes a candidate coherent; training determines whether it improves the model.

The design rule is direct: **derive geometry from the invariances, growth laws, task distinctions, and operations that need to be preserved.** Those requirements make a geometric choice testable.

(011-geometry-from-invariance-sources)=
## Sources and chronology
- [Milestone notebook 011 — preserved chronological source](../notebooks/011_geometry_from_invariance.ipynb)
- [Research chronology](../CHRONOLOGY.md)
- [Publication dispositions and Atlas-to-article map](../PUBLICATION-DISPOSITIONS.md)

The matching Atlas theme is **Radius–angle coupling**. The original [Visual Intuition Atlas notebook](../notebooks/visual_intuition_atlas.ipynb) remains available as a source record; this article carries the relevant static explanation inline.

The next chronological article is [**Milestone 012 — Natural-source task distinctions**](./012-natural-source-distinctions.md).
