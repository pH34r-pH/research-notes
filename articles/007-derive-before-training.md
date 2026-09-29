---
title: "Milestone 007 — Derive before training"
description: "What can we prove about normalization before spending compute?"
short_title: "Derive before training"
date: 2026-09-29
authors:
  - name: Tyler J.H.G.
tags:
  - research milestone
  - executable article
---

(milestone-007)=
# Milestone 007 — Derive before training
**Research period:** September 2–3, 2026 and later formal hardening  
**Historical anchors:** #196, #199, #200, #252

The hypersphere experiments generated several possible explanations for what normalization might be doing: removing an unnecessary magnitude channel, changing optimization, suppressing shortcuts, preserving some directions while contracting others, or changing the long-term dynamics of recurrence. At this point, simply training another model for every plausible explanation was becoming a bad research strategy.

Some of these questions had mathematical answers that could be established before running another experiment. If a proposed mechanism depended on normalization behaving a particular way, I could derive that behavior first and use the result to decide which empirical questions were still meaningful.

That became the beginning of a proof-first layer in the research program: derive what can be derived, keep the assumptions and boundaries explicit, then spend compute on the parts the mathematics cannot decide.

> **Formal checkpoint:** for a nonzero vector `x`, normalization is `N(x) = x / ||x||`. If `u = x / ||x||`, its derivative is
>
> `DN_x = (1 / ||x||)(I - uuᵀ)`
>
> The checked version is available in the public [Theorem Library normalization proof](https://github.com/pH34r-pH/theorem-library/blob/2c90ec3d482a64a5bce5787f48c5828429c50305/TheoremLibrary/Geometry/Sphere/Normalization.lean).

(007-derive-before-training-visual-intuition)=
## Visual intuition
```{figure} ./007_derive_before_training.svg
:label: 007-derive-before-training-intuition
:alt: At a nonzero point, normalization removes first-order radial change and rescales tangent change.

At a nonzero input, the derivative of normalization removes radial change and rescales tangent change.
```

## Radial and tangent directions

The expression `I - uuᵀ` is a projection: it removes the part of a small change that points in the same direction as `u`.

That gives normalization two different local behaviors. If I perturb `x` only by changing its magnitude, the normalized direction doesn't change to first order, so the derivative of that radial perturbation is zero. If I perturb `x` perpendicular to its radius, the change lies along the surface of the sphere and survives, scaled by `1 / ||x||`. At unit radius, that tangent perturbation is preserved to first order.

> **Sticky note — tangent direction:** at a point on a sphere, a tangent direction is perpendicular to the radius through that point. Locally, these are the directions in which you can move along the surface rather than toward or away from its center.

This gave me an exact version of something the earlier experiments had only suggested. Normalization really does remove infinitesimal changes that affect only overall scale while allowing changes in direction to survive locally.

The useful part was the boundary around that statement. The mathematics says **what normalization does to perturbations**; it doesn't say what those perturbations mean to a language model.

## Try a small example

A two-dimensional example separates radial and tangent perturbations. Try changing the point and perturbation vectors. The saved output below is available without starting Python.

```{code-cell} python
:label: 007-derive-before-training-teaching-example
:tags: [illustrative, thebe]

import numpy as np
x = np.array([3., 4.]); r=np.linalg.norm(x); u=x/r
DN = (np.eye(2)-np.outer(u,u))/r
radial = u
tangent = np.array([-u[1], u[0]])
print('radial derivative:', DN @ radial)
print('tangent gain:', np.linalg.norm(DN @ tangent))
```

**Saved output:**

```text
radial derivative: [-8.39328607e-18 -1.45217172e-17]
tangent gain: 0.2
```


## What this changed

That distinction became a template for the next stage of the project.

Suppose an experiment suggests that normalization helps because magnitude contains nuisance variation while direction carries useful information. The derivative above can prove that normalization removes radial variation locally. It cannot prove that radial variation is nuisance information, or that tangent variation contains semantics. Those are properties of the task, representation, and trained model, so they still require measurement.

Separating those two kinds of claims prevents an appealing geometric interpretation from quietly turning into an empirical conclusion.

This also changed how I thought about experiment design. A proposed architecture can depend on assumptions that are already mathematically true, mathematically false, or true only under specific conditions. Deriving those boundaries first can eliminate experiments whose premises are impossible, simplify experiments whose mechanisms are already known, and leave training for questions that genuinely depend on learned behavior.

The resulting workflow became:

`hypothesis → derivation / theorem boundary → surviving empirical question → experiment`

rather than treating training as the default way to answer every question.

## Research context

This proof-first turn also brought the project closer to a broader body of geometric machine-learning research. Work such as **nGPT** had already shown that Transformer computation could be formulated around normalized states on a hypersphere, so normalization and hyperspherical optimization themselves weren't new ideas. The useful question for this project was narrower: what could the exact mathematics tell me about the mechanism behind the behavior I had already measured?

The literature provided established constructions and mathematical neighborhoods to compare against; the theorem work gave me a way to separate those established facts from claims that were still specific to this representation and task.

## Interpretation

The derivative establishes a local, first-order effect: radial perturbations vanish, and tangent perturbations scale by inverse radius. Whether either direction carries useful task information has to be measured in the trained model.

Repeated nonlinear updates also require analysis beyond a single derivative. The calculation gives later mechanism explanations a concrete constraint and points toward finite-horizon diagnostics.

## Public formal sources

- [Normalization](https://github.com/pH34r-pH/theorem-library/blob/2c90ec3d482a64a5bce5787f48c5828429c50305/TheoremLibrary/Geometry/Sphere/Normalization.lean)
- [NormalizationSpectrum](https://github.com/pH34r-pH/theorem-library/blob/2c90ec3d482a64a5bce5787f48c5828429c50305/TheoremLibrary/Geometry/Sphere/NormalizationSpectrum.lean)

These pinned sources state the assumptions and checked mathematical conclusions.

(007-derive-before-training-sources)=
## Sources and chronology
- [Milestone notebook 007 — preserved chronological source](../notebooks/007_derive_before_training.ipynb)
- [Research chronology](../CHRONOLOGY.md)
- [Publication dispositions and Atlas-to-article map](../PUBLICATION-DISPOSITIONS.md)

The matching Atlas theme is **Normalization derivative**. The original [Visual Intuition Atlas notebook](../notebooks/visual_intuition_atlas.ipynb) remains available as a source record; this article carries the relevant static explanation inline.

The next chronological article is [**Milestone 008 — What does the sphere actually do?**](./008-frozen-mechanism-tests.md).
