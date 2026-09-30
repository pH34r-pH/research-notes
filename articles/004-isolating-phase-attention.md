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

The polar-native block improved the result, but it bundled several changes together: explicit magnitude handling, phase-preserving residual connections, and phase-aware attention. I needed to separate them before building further work around the block.

I used ablations: remove or replace one component, rerun the matched comparison, and check which gains survive. If a component can be removed without losing the improvement, the explanation has to work without it.

> **Sticky note — ablation:** remove or replace one component while keeping the rest of the system as unchanged as possible. The comparison tests how much the result depends on that component. [Reference →](../reference/glossary.md#ablation)

(004-isolating-phase-attention-visual-intuition)=
## Visual intuition
```{figure} ./004_isolating_phase_attention.svg
:label: 004-isolating-phase-attention-intuition
:alt: A phase circle relates relative angle to normalized real-Hermitian similarity.

The cosine of the relative phase gives normalized real-Hermitian similarity.
```

## What survived

Phase/Hermitian attention retained the approximately **0.3923 nat per original byte** improvement over the coordinate-only control.

The phase-preserving residual connection alone failed to clear the predefined statistical and materiality requirements. Explicit log-radius handling produced results bit-identical to its matched manual control. Neither supplied an independent explanation for the improvement.

That left a much smaller construction: an otherwise mostly Cartesian block using normalized real-Hermitian similarity to compare attention queries and keys. Relative phase entered the attention score directly; the rest of the polar-native machinery could be removed.

> **Sticky note — Hermitian similarity:** a Hermitian inner product conjugates one complex vector before comparing it with the other, so relative phase contributes to the result. Here, I take its real component and normalize by the vector magnitudes to obtain the attention similarity score.

## Try a small example

Two hand-chosen complex vectors show how relative phase affects similarity.

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

The ablation isolated phase-aware similarity as the component carrying the improvement in this spectral comparison. Hermitian and phase-aware attention already have precedents; this experiment identified which part was useful in the system I was testing.

I could freeze that component and move on to recurrence. Further comparisons would then change the recurrent state without also changing the attention mechanism.

(004-isolating-phase-attention-sources)=
## Sources and chronology
- [Milestone notebook 004 — preserved chronological source](../notebooks/004_isolating_phase_attention.ipynb)
- [Research chronology](../CHRONOLOGY.md)
- [Publication dispositions and Atlas-to-article map](../PUBLICATION-DISPOSITIONS.md)

The matching Atlas theme is **Phase-aware similarity**. The earlier [Visual Intuition Atlas notebook](../notebooks/visual_intuition_atlas.ipynb) preserves the source visualization.

The next chronological article is [**Milestone 005 — The unit-hypersphere anomaly**](./005-unit-hypersphere-anomaly.md).
