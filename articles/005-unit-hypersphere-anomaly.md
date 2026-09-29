---
title: "Milestone 005 — The unit-hypersphere anomaly"
description: "What happens when recurrent state keeps direction but discards magnitude?"
short_title: "The unit-hypersphere anomaly"
date: 2026-09-29
authors:
  - name: Tyler J.H.G.
tags:
  - research milestone
  - executable article
---

(milestone-005)=
# Milestone 005 — The unit-hypersphere anomaly
**Research period:** September 1–2, 2026  
**Historical anchor:** #164

With the phase-aware attention mechanism isolated, I could freeze it and move on to a different question: what should happen to the representation as it passes repeatedly through the model?

I compared ordinary independent depth, shared recurrent computation, recurrence constrained to the unit hypersphere, and a related version that retained radius as an additional degree of freedom. I initially expected retaining radius to help; magnitude seemed like potentially useful information, and forcing every state onto the unit hypersphere deliberately throws that information away.

Instead, the direction-only model produced the strongest endpoint by a large margin.

> **Sticky note — unit hypersphere:** a vector is constrained to have length 1, so its direction can change while its overall magnitude cannot. In d dimensions, these unit-length vectors form the surface of a hypersphere.

(005-unit-hypersphere-anomaly-visual-intuition)=
## Visual intuition
```{figure} ./005_unit_hypersphere_anomaly.svg
:label: 005-unit-hypersphere-anomaly-intuition
:alt: A vector is projected onto the unit circle. This simple geometric example is not a training result.

This is a synthetic vector normalization example. It does not reproduce the frozen training endpoint.
```

## Frozen endpoint

After 128 training updates, validation negative log-likelihood (NLL) per original byte was approximately:

- depth-1 anchor: **5.1371**
- independent depth-3: **5.7188**
- shared generic depth-3: **5.1569**
- unit-hypersphere depth-3: **3.6584**
- retained-radius depth-3: **5.1225**

Lower NLL is better, so the unit-hypersphere model beat the otherwise comparable shared recurrent model by about **1.50 nats per byte** at this endpoint. Retaining radius didn't reproduce the improvement.

This was surprising enough to change the direction of the investigation. The result contradicted my original expectation that magnitude would provide a useful additional degree of freedom, and the size of the gap made the unit constraint worth investigating directly.

There was an immediate reason to be cautious, though: the unit model learned more slowly, and its area under the learning curve (AULC) was worse even though its final measured point was dramatically better.

> **Sticky note — AULC:** area under the learning curve summarizes performance across the training trajectory rather than at one selected endpoint. A model can finish ahead while having performed worse for much of training.

## A small editable teaching example

This two-dimensional vector demonstrates normalization. It does not reproduce the training result described above.

Saved output is included so you can inspect the example without starting a kernel. Activating the code cell below runs this synthetic example only.

```{code-cell} python
:label: 005-unit-hypersphere-anomaly-teaching-example
:tags: [illustrative, thebe]

import numpy as np
x = np.array([3.0, 4.0])
u = x / np.linalg.norm(x)
print('unit state:', u, 'norm=', np.linalg.norm(u))
# Normalization deliberately removes one scalar degree of freedom: overall scale.
```

**Published teaching output (synthetic):** the saved notebook output below belongs only to the small code example. It is not a replay of historical model training.

```text
unit state: [0.6 0.8] norm= 1.0
```


## What this does not show

The endpoint result was an anomaly to explain, not evidence that hyperspherical models are generally better. Constraining every state to unit length changes several things simultaneously: capacity, numerical conditioning, vector norms, rank dynamics, optimization, and the geometry available to the model. Any of those changes could contribute to the result.

The retained-radius control ruled out one simple explanation I had expected to work. If explicit magnitude were responsible for the advantage, preserving it should have retained the effect; it didn't. That made the strict direction-only constraint itself more interesting, but still didn't tell me why it helped.

The learning trajectory created another problem. A single endpoint can make a model look dramatically better while hiding slower learning earlier in training, so I couldn't treat the 128-update comparison as evidence that the unit model dominated across training budgets.

One particularly important alternative remained: normalization might simply be acting as unusually strong regularization. Before attributing the result to hyperspherical geometry or to a special relationship with the spectral representation, I needed to separate those possibilities.

(005-later-muon-package)=
## A later packaged comparison is related, not a replay
A later three-seed Muon comparison reused the `unit_hypersphere_depth3` condition and compared Muon against the corresponding **frozen historical AdamW** results. Its reviewed record reports different directions at the two endpoints: the learning-curve area favors the historical AdamW control, while final NLL favors Muon. It calls the overall outcome mixed/inconclusive and does not claim an optimizer winner.

That package is a real, finalized, inspectable Compiled Experiment, but it does **not** rerun the #164 topology selection or independently reproduce the 128-update anomaly above. It is linked as later model-condition context, not as a substitute for the missing exact #164 endpoint package: [inspect the exact Muon multi-seed package](https://experiments.tyharbin.com/experiments/muon-unit-hypersphere-depth3-multiseed-v1-final-87409154/).

(005-unit-hypersphere-anomaly-sources)=
## Sources and chronology
- [Milestone notebook 005 — preserved chronological source](../notebooks/005_unit_hypersphere_anomaly.ipynb)
- [Research chronology](../CHRONOLOGY.md)
- [Publication dispositions and Atlas-to-article map](../PUBLICATION-DISPOSITIONS.md)

The matching Atlas theme is **Unit-sphere normalization**. The original [Visual Intuition Atlas notebook](../notebooks/visual_intuition_atlas.ipynb) remains available as a source record; this article carries the relevant static explanation inline.

The next chronological article is [**Milestone 006 — A dramatic endpoint can still mislead**](./006-endpoint-can-mislead.md).
