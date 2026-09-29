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
:alt: Toy vector normalization projects a vector onto the unit circle while preserving its direction.

Toy normalization: projecting a vector onto the unit circle preserves its direction and removes its scale.
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

The learning trajectory told a different story: the unit model learned more slowly and had worse area under the learning curve (AULC), despite its better endpoint.

> **Sticky note — AULC:** area under the learning curve summarizes performance across the training trajectory rather than at one selected endpoint. A model can finish ahead while having performed worse for much of training.

## Try a small example

The toy vector `[3, 4]` makes normalization easy to inspect: its length is 5, and its unit direction is `[0.6, 0.8]`. The saved output below is available without starting Python.

```{code-cell} python
:label: 005-unit-hypersphere-anomaly-teaching-example
:tags: [illustrative, thebe]

import numpy as np
x = np.array([3.0, 4.0])
u = x / np.linalg.norm(x)
print('unit state:', u, 'norm=', np.linalg.norm(u))
# Normalization deliberately removes one scalar degree of freedom: overall scale.
```

**Saved output:**

```text
unit state: [0.6 0.8] norm= 1.0
```


## Interpretation

The unit constraint produced a large endpoint advantage while learning more slowly. It also changed capacity, conditioning, rank dynamics, and optimization together, leaving several explanations open.

The retained-radius control weakened the explanation I had expected: preserving explicit magnitude failed to preserve the effect. The next question was whether strict normalization supplied a useful geometric constraint or simply acted as strong regularization. Answering it required trajectory analysis and a matched regularization control.

(005-later-muon-package)=
## Later Muon comparison
A later three-seed comparison tested Muon on the `unit_hypersphere_depth3` condition against **frozen historical AdamW** results. Learning-curve area favored AdamW; final NLL favored Muon. The reviewed outcome was **mixed/inconclusive**.

[Inspect the finalized Muon multi-seed package](https://experiments.tyharbin.com/experiments/muon-unit-hypersphere-depth3-multiseed-v1-final-87409154/). It addresses optimizer behavior on this model condition; the #164 topology-selection experiment above remains a separate comparison.

(005-unit-hypersphere-anomaly-sources)=
## Sources and chronology
- [Milestone notebook 005 — preserved chronological source](../notebooks/005_unit_hypersphere_anomaly.ipynb)
- [Research chronology](../CHRONOLOGY.md)
- [Publication dispositions and Atlas-to-article map](../PUBLICATION-DISPOSITIONS.md)

The matching Atlas theme is **Unit-sphere normalization**. The original [Visual Intuition Atlas notebook](../notebooks/visual_intuition_atlas.ipynb) remains available as a source record; this article carries the relevant static explanation inline.

The next chronological article is [**Milestone 006 — A dramatic endpoint can still mislead**](./006-endpoint-can-mislead.md).
