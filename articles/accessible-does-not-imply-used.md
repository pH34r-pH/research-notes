---
title: "Milestone 013 — Accessible does not imply used"
description: A frozen-representation probe found a natural-source distinction that the model's native consumer barely used.
short_title: Accessible does not imply used
date: 2026-09-29
authors:
  - name: Tyler J.H.G.
tags:
  - representation learning
  - probing
  - utilization
---

(milestone-013)=
# Milestone 013 — Accessible does not imply used
**Research period:** September 8–9, 2026  
**Public article source revision:** September 29, 2026  
**Historical anchor:** #328  
**Primary source:** [Milestone notebook 013](../notebooks/013_accessible_not_used.ipynb)

(accessible-used-question)=
## The question
The revision-branch benchmark provided a task where preserving a distinction mattered. Returning to the compact, unit-hypersphere representation, the next question was whether the branch information had been erased or remained present while the model's own consumer failed to use it.

Those explanations imply different interventions. If the representation has lost the distinction, changing only the final readout cannot recover it. If a simple readout can recover it from a frozen state, the bottleneck may instead lie in how the native consumer combines that state into a prediction.

The experiment froze the representation and compared a deliberately small affine-softmax probe with the model's frozen native consumer. The probe was diagnostic: it tested recoverability under a bounded readout family. It was not inserted into the model and did not alter the historical run.

## What the probe measured

For a frozen hidden state $h$, the probe computes logits

$$
z = Wh + b, \qquad p(y\mid h)=\operatorname{softmax}(z).
$$

This is an affine map followed by a probability readout. It can combine and reweight existing coordinates, but it adds no nonlinear representation layer. Success on held-out examples therefore supports a narrow statement: the tested natural-source branch distinction was accessible to this simple external consumer.

The reported quantity is evaluation log-loss gain over a constant baseline,

$$
G = L_{\mathrm{constant}} - L_{\mathrm{consumer}},
$$

so positive values indicate lower evaluation loss than the baseline. The source notebook reports the following comparison:

```{figure} ./accessible-vs-used.svg
:label: accessible-vs-used
:alt: Horizontal comparison of the reported natural-source benchmark log-loss gains. The affine-softmax probe gained 0.737664 nat, with a one-sided lower confidence bound of 0.678 nat. The frozen native consumer gained 0.006446 nat. The values share the constant-baseline reference; the figure does not show a full next-byte result.

On the frozen natural-source branch benchmark, a small external readout recovered substantially more of the tested distinction than the model's own consumer.
```

| Consumer | Evaluation log-loss gain over constant baseline | Evidence boundary |
| --- | ---: | --- |
| Affine-softmax probe | 0.737664 nat; one-sided lower confidence bound about 0.678 nat | External, separately trained probe on the frozen representation |
| Frozen native consumer | 0.006446 nat | The model's original downstream consumer on the same bounded branch task |

The tangent-coordinate analysis reached the same qualitative conclusion, so the probe did not depend on an obvious radial coordinate. Selectivity controls also passed. The result was classified as **ACCESSIBLE-BUT-UNDERUSED**.

## Inspect the geometry

The representation is constrained to a unit hypersphere. A point on that sphere has a local tangent space, and a probe selects a direction along which it reads out variation. The plot below is a **synthetic two-dimensional analogy**, not measured model coordinates.

```{figure} ./unit-circle-readout.svg
:label: unit-circle-readout
:alt: Synthetic unit-circle slice with a fixed signal direction and an aligned readout direction. The geometry is illustrative, not measured model coordinates.

In a 2D slice, the signal and readout directions align, so the projection is 1.00. When JavaScript is available, a slider appears below the figure so readers can rotate the readout and inspect the projection. The control's values are synthetic and are not benchmark measurements.
```

For a unit vector $h$, the tangent projector is $P_h=I-hh^\top$. More generally, for nonzero $h$,

$$
P_h = I - \frac{hh^\top}{\lVert h\rVert^2}.
$$

This defines a geometric projection onto directions tangent to the sphere at $h$. It does not assign semantic meaning to any direction. The frozen-model experiment's tangent-coordinate analysis is an empirical control; the normalization theorem is separate mathematical context. **Formal checkpoint — LIB-SPH-002 / FRM-000020:** the derivative of nonzero normalization annihilates radial perturbations and scales tangent perturbations by inverse radius. That theorem establishes a local property of a mathematical map; it does not explain why this trained model used or ignored a particular signal. See the [formal reference](../reference/formal-methods/checkpoints.md) and the [theorem source at the reviewed revision `14ff466c4dabb3a9a09717d65236832b7ff3a26e`](https://github.com/pH34r-pH/theorem-library/blob/14ff466c4dabb3a9a09717d65236832b7ff3a26e/TheoremLibrary/Geometry/Sphere/Anisotropy.lean).

## Why a successful probe is not enough

A flexible diagnostic can exploit quirks of a dataset, memorize labels, or discover a signal that the native model ignores. Probe accuracy by itself cannot distinguish those cases. The probing literature treats that capacity problem in different ways: control-task selectivity asks whether a probe succeeds on the intended structure while failing when it is destroyed; information-theoretic and minimum-description-length approaches ask related but different questions about recoverable information and the cost of encoding the probe's solution [@hewitt2019designing; @pimentel2020information; @voita2020mdl].

The original analysis used label shuffles, representation shuffles, matched random features, random rotations, fixed page groups, and learning-efficiency checks as controls. Each challenged a different alternative explanation, including accidental label structure, memorization, coordinate artifacts, source leakage, and a procedure that would find apparent signal almost anywhere. The tangent-coordinate analysis specifically addressed radial-versus-tangent confounding raised by the earlier unit-hypersphere work.

The conclusion is therefore bounded by the tested task, data, probe family, and controls. It is not a statement that the representation is universally sufficient or that every affine probe will recover every task-relevant property.

## A small editable teaching example

The cell below is a deterministic synthetic demonstration. It constructs toy states with a simple class signal and reports how a chosen readout direction classifies those states. Changing `probe_degrees` changes only the synthetic consumer. It does not use the frozen research model, the historical benchmark, or private inputs.

```{code-cell} python
:label: synthetic-readout
:tags: [illustrative, thebe]

import math

states = [
    (0.9, 0.1), (0.7, -0.3), (0.6, 0.2),
    (-0.9, -0.1), (-0.7, 0.3), (-0.6, -0.2),
]
labels = [1, 1, 1, -1, -1, -1]
probe_degrees = 0
angle = math.radians(probe_degrees)
weights = (math.cos(angle), math.sin(angle))
correct = sum(
    ((1 if state[0] * weights[0] + state[1] * weights[1] >= 0 else -1) == label)
    for state, label in zip(states, labels)
)
print(f"synthetic teaching accuracy: {correct / len(labels):.0%}")
```

**Published teaching output (synthetic):** with `probe_degrees = 0`, the example reports 100%. This value is only the output of the tiny fixed teaching set above; it is neither the 0.737664-nat historical probe gain nor a model benchmark.

When activated, the article cell can be edited and run in a browser-local JupyterLite session. That output is labeled **Your session** and cannot replace the published teaching output above.

## What this does not show

- Probe success does not establish that the native model causally uses the recovered information.
- This branch task does not show that the frozen representation contains everything needed for language modeling or the complete next-byte task.
- Predicting a revision branch is much easier than predicting one of 256 possible next-byte values. The binary branch signal may not convert into a useful full-distribution prediction.
- The synthetic geometry and teaching cell do not replay or qualify the historical benchmark.
- The exact frozen-model benchmark replay is not included in the public notebook or this article. There is no exact public Compiled Experiment package for this benchmark in the current catalog, so this article does not link to a different experiment as a substitute.

## The next experiment

Keep the representation frozen, but move closer to the actual objective: train a ladder of very small consumers on the 256-way next-byte task. The open question is how much of the signal accessible to a small probe can be converted into useful full-distribution prediction.

## Sources and chronology

- [Milestone notebook 013 — primary historical account](../notebooks/013_accessible_not_used.ipynb)
- [Milestone 012 — Natural-source task distinctions](../notebooks/012_natural_source_distinctions.ipynb)
- [Milestone 008 — What does the sphere actually do?](../notebooks/008_frozen_mechanism_tests.ipynb)
- [Visual Intuition Atlas — probe recoverability and normalization geometry](../notebooks/visual_intuition_atlas.ipynb)
- [Representation and Readout reference](../reference/representation-and-readout.md)
- [Research chronology](../CHRONOLOGY.md)


(accessible-used-publication-map)=
## Publication map
See the [Research Notes publication dispositions](../PUBLICATION-DISPOSITIONS.md) for the complete article/source classification.
