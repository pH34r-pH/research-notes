---
title: "Milestone 004 — Isolating the phase-aware mechanism"
description: "Which part of phase-aware attention accounts for the improvement?"
short_title: "Isolating the phase-aware mechanism"
date: 2026-09-29
authors:
  - name: Tyler J.H.G.
tags:
  - research milestone
  - executable article
---

(milestone-004)=
# Milestone 004 — Isolating the phase-aware mechanism
**Research period:** September 1, 2026  
**Historical anchor:** #163

The previous experiment showed that changing the downstream computation could make the same spectral representation substantially more useful, but I had changed several things at once. The model handled magnitude explicitly, preserved phase through residual connections, and used phase-aware similarity in attention. Any one of those changes (or an interaction between them) could have been responsible for the improvement.

I separated those components through ablation: remove or replace one part of the architecture, rerun the comparison, and see which gains survive.

> **Sticky note — ablation:** an experiment that removes or replaces one component while leaving the rest of the system as unchanged as possible. If the effect disappears, that component becomes a candidate explanation for the original result. [Reference →](../reference/glossary.md#ablation)

(004-isolating-phase-attention-visual-intuition)=
## Visual intuition
```{figure} ./004_isolating_phase_attention.svg
:label: 004-isolating-phase-attention-intuition
:alt: A phase circle relates relative angle to normalized real-Hermitian similarity.

The cosine of the relative phase gives normalized real-Hermitian similarity.
```

## What survived

The phase-aware attention mechanism survived the ablation. Compared with the coordinate-only control, phase/Hermitian attention improved loss by about **0.3923 nat per original byte**.

The other candidate explanations didn't survive in the same way. A phase-preserving residual connection by itself didn't clear the predefined statistical and materiality requirements, while explicit log-radius handling produced results that were bit-identical to its matched manual control.

This narrowed the result considerably. I no longer needed a broadly “polar-native” architecture to explain the improvement; the smallest surviving change was an otherwise mostly Cartesian processing block using normalized real-Hermitian similarity for the attention query/key comparison.

> **Sticky note — Hermitian similarity:** complex vectors contain both magnitude and phase. A Hermitian inner product conjugates one of its inputs before comparing them, allowing their relative phase to contribute naturally to the result. Taking the real component and normalizing by vector magnitude produces the similarity score used here.

## Try a small example

Two hand-chosen complex vectors show how relative phase affects similarity. The saved output below is available without starting Python.

```{code-cell} python
:label: 004-isolating-phase-attention-teaching-example
:tags: [illustrative, thebe]

import numpy as np
q = np.array([1+1j, 1-1j])
k = np.array([1+0j, 0+1j])
score = np.real(np.vdot(q, k)) / (np.linalg.norm(q)*np.linalg.norm(k))
print('normalized real-Hermitian similarity:', score)
```

**Saved output:**

```text
normalized real-Hermitian similarity: 0.0
```


## Interpretation

The ablation identified phase-aware similarity as the component carrying the improvement for this spectral representation. Hermitian and phase-aware attention have established precedents; the contribution here was isolating their role in this comparison. I could now freeze that component and study recurrence without changing the whole architecture again.

(004-isolating-phase-attention-sources)=
## Sources and chronology
- [Milestone notebook 004 — preserved chronological source](../notebooks/004_isolating_phase_attention.ipynb)
- [Research chronology](../CHRONOLOGY.md)
- [Publication dispositions and Atlas-to-article map](../PUBLICATION-DISPOSITIONS.md)

The matching Atlas theme is **Phase-aware similarity**. The original [Visual Intuition Atlas notebook](../notebooks/visual_intuition_atlas.ipynb) remains available as a source record; this article carries the relevant static explanation inline.

The next chronological article is [**Milestone 005 — The unit-hypersphere anomaly**](./005-unit-hypersphere-anomaly.md).
