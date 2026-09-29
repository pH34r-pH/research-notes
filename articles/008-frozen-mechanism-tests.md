---
title: "Milestone 008 — What does the sphere actually do?"
description: "Which proposed mechanisms survive frozen tests of the model’s dynamics?"
short_title: "What does the sphere actually do?"
date: 2026-09-29
authors:
  - name: Tyler J.H.G.
tags:
  - research milestone
  - executable article
---

(milestone-008)=
# Milestone 008 — What does the sphere actually do?
**Research period:** September 3–5, 2026  
**Historical anchors:** #201–#206

The normalization derivative gave me an exact local fact, but several empirical explanations were still compatible with it. The unit constraint might be removing a harmful magnitude channel, suppressing an easy shortcut, selectively preserving useful tangent directions, or changing how perturbations accumulate through recurrent depth.

I could test much of this without training anything new. Instead, I treated the frozen model as an object to intervene on: change its radius, measure radial and tangent sensitivity, follow perturbations through several recurrent steps, test whether those perturbations reach the output, and probe what information is accessible in different parts of the state.

This kept the question narrow. If the existing model already contradicted a proposed mechanism, there was no reason to build another model around it.

(008-frozen-mechanism-tests-visual-intuition)=
## Visual intuition
```{figure} ./008_frozen_mechanism_tests.svg
:label: 008-frozen-mechanism-tests-intuition
:alt: A small per-step contraction compounds across recurrent steps; actual finite-horizon effects depend on the sequence of Jacobians.

A toy scalar contraction compounds across steps. In a recurrent model, the full calculation uses a sequence of Jacobians.
```

## The mechanism campaign

The tests produced a deliberately untidy result:

- radius interventions: **MIXED**
- radial/tangent Jacobian analysis: **RADIAL-WEAK**
- finite-horizon Jacobian products: **NO-SPECTRAL-SEPARATION**
- output sensitivity: **RADIAL-LOCALLY-ACTIVE**
- information probes: **MIXED**

The labels summarize different questions, so they aren't supposed to collapse into one vote.

Changing radius affected some measurements but didn't reveal a simple monotonic mechanism. Local derivatives showed weaker radial response than tangent response, which was consistent with the normalization theorem. Across several recurrent steps, however, the accumulated Jacobians didn't produce the clean spectral separation I would have expected from a strong selective-contraction story.

At the output, radial perturbations could still matter locally. That was an important boundary: normalization suppressing radial variation at one point in the computation didn't imply that every radius-related degree of freedom elsewhere in the model was irrelevant.

The probes were similarly mixed. They didn't support a clean story in which radius was either a uniquely useful signal or an obvious harmful shortcut.

> **Sticky note — Jacobian:** a Jacobian describes how small changes in a model's input or internal state change its output locally. Looking at different input directions lets us ask whether the model is more sensitive to some perturbations than others.

> **Sticky note — finite-horizon Jacobian:** in a recurrent model, small changes pass through several successive updates. Multiplying the Jacobians of those updates tells us how a perturbation propagates across that finite sequence rather than through only one step.

## Try a small example

Two hand-chosen matrices show how local Jacobians combine over a finite horizon. The saved output below is available without starting Python.

```{code-cell} python
:label: 008-frozen-mechanism-tests-teaching-example
:tags: [illustrative, thebe]

import numpy as np
J0=np.diag([0.5,1.0]); J1=np.array([[1.,0.2],[0.,0.8]])
J10=J1@J0
print('finite-horizon Jacobian:\n',J10)
print('singular values:',np.linalg.svd(J10,compute_uv=False))
```

**Saved output:**

```text
finite-horizon Jacobian:
 [[0.5 0.2]
 [0.  0.8]]
singular values: [0.83792489 0.47736976]
```


## Why there wasn't a sixth experiment

The original mechanism plan allowed another training experiment if the frozen diagnostics identified a question that required one. After reviewing the results, I didn't run it.

The proposed control was supposed to create a model that ignored radius while remaining meaningfully different from the existing unit-hypersphere model. Once specified carefully enough to be a faithful control, it collapsed to essentially the model I had already tested. Training it again wouldn't separate the competing explanations.

That made **not running the experiment** the correct result of the analysis. Compute wasn't the main concern; causal identifiability was. A new training run is only useful if its outcomes can distinguish the hypotheses we care about.

## Research context

This part of the investigation drew increasingly on dynamical-systems and sensitivity-analysis ideas. A one-step derivative describes local behavior, while products of derivatives along a trajectory describe how those local effects accumulate through recurrent computation. That distinction matters because a recurrent network can amplify, rotate, cancel, or redistribute a perturbation even when the first local response looks simple.

The literature provided tools for asking those questions, but I kept the claims tied to the finite trained system in front of me. A local normalization theorem, a finite-horizon Jacobian calculation, and a statement about asymptotic recurrent dynamics are different results; none should silently stand in for the others.

## Interpretation

The frozen diagnostics gave mixed support for the tested radial-shortcut and selective-contraction explanations. Local sensitivity established influence under an intervention; held-out prediction was still needed to establish usefulness.

The proposed extra control collapsed to the model already tested. Rejecting that redundant comparison was the practical result: the analysis eliminated a training run that would have added a number without separating the hypotheses.

## Public formal sources

- [NormalizationComposition](https://github.com/pH34r-pH/theorem-library/blob/2c90ec3d482a64a5bce5787f48c5828429c50305/TheoremLibrary/Geometry/Sphere/NormalizationComposition.lean)
- [RadialMemory](https://github.com/pH34r-pH/theorem-library/blob/2c90ec3d482a64a5bce5787f48c5828429c50305/TheoremLibrary/Geometry/Sphere/RadialMemory.lean)

These pinned sources state the assumptions and checked mathematical conclusions.

(008-frozen-mechanism-tests-sources)=
## Sources and chronology
- [Milestone notebook 008 — preserved chronological source](../notebooks/008_frozen_mechanism_tests.ipynb)
- [Research chronology](../CHRONOLOGY.md)
- [Publication dispositions and Atlas-to-article map](../PUBLICATION-DISPOSITIONS.md)

The matching Atlas theme is **Finite-horizon Jacobian products**. The original [Visual Intuition Atlas notebook](../notebooks/visual_intuition_atlas.ipynb) remains available as a source record; this article carries the relevant static explanation inline.

The next chronological article is [**Milestone 009 — From hypothesis sprawl to a theorem ledger**](./009-theorem-ledger-method.md).
