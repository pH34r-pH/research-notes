---
title: "Milestone 003 — Coordinates matter; operations matter more"
description: "Does changing coordinates help, or do the operations need to change too?"
short_title: "Coordinates matter; operations matter more"
date: 2026-09-29
model_focus: architecture
model_variant: phase-aware
depends_on: [002-locating-representation-loss]
authors:
  - name: Tyler J.H.G.
tags:
  - research milestone
  - executable article
---

(milestone-003)=
# Milestone 003 — Coordinates matter; operations matter more
**Research period:** September 1, 2026  
**Historical anchors:** #161–#162

The stage comparison suggested that the consumer was struggling with the spectral state even before composition. I held that uncombined state fixed and changed how the downstream model represented and processed it.

There were two effects to separate. We can rewrite a complex value as `[rho, cos(theta), sin(theta)]` and still apply roughly the same computation. We can also change the computation to operate directly on magnitude and relative phase. The first is a change of coordinates; the second gives the model different operations on the same underlying information.

A coordinate-only control let me measure how much each change contributed.

> **Sticky note — log-polar:** describe a complex value using its magnitude and angle. Here, `rho = log(|z| + eps)` puts magnitude on a logarithmic scale, and `theta` is its phase.

(003-coordinates-and-matched-operations-visual-intuition)=
## Visual intuition
```{figure} ./003_coordinates_and_matched_operations.svg
:label: 003-coordinates-and-matched-operations-intuition
:alt: A conceptual complex-plane diagram separates coordinate re-expression from changing the downstream operation.

Toy complex values can be re-expressed in polar coordinates. Changing the operation is a separate choice.
```

## Result

Both changes improved loss. The coordinate-only representation helped, and the polar-native processing path improved it further.

Relative to spectral Cartesian processing, the polar-native model improved loss by about **0.5825 nat per original byte**. Relative to the coordinate-only control, which contained the same underlying information, it improved loss by about **0.3923 nat per original byte**. All three experimental seeds cleared the predefined materiality threshold.

The second comparison is the one that matters for the mechanism. Re-expressing the state accounts for part of the improvement; changing the operations accounts for an additional part. I could now investigate the polar-native block itself.

## Try a small example

Three hand-chosen complex values show how Cartesian and polar coordinates describe the same information.

```{code-cell} python
:label: 003-coordinates-and-matched-operations-teaching-example
:tags: [illustrative, thebe]

import numpy as np
z = np.array([1+1j, -2+0.5j, 0.2-3j])
rho = np.log(np.abs(z) + 1e-8)
phase_features = np.c_[rho, np.cos(np.angle(z)), np.sin(np.angle(z))]
print(phase_features)
```

**Saved output:**

```text
[[ 0.3465736   0.70710678  0.70710678]
 [ 0.7234595  -0.9701425   0.24253563]
 [ 1.10082959  0.06651901 -0.99778516]]
```


## Interpretation

The coordinate-only control gave me a baseline for the benefit of re-expression. The polar-native block beat that baseline, but several operations inside it had changed together.

The next step was to remove those changes one at a time, keeping the source representation fixed. Which operation would preserve the additional gain?

(003-coordinates-and-matched-operations-sources)=
## Sources and chronology
- [Milestone notebook 003 — preserved chronological source](../notebooks/003_coordinates_and_matched_operations.ipynb)
- [Research chronology](../CHRONOLOGY.md)
- [Publication dispositions and Atlas-to-article map](../PUBLICATION-DISPOSITIONS.md)

The matching Atlas theme is **Phase-aware coordinates**. The earlier [Visual Intuition Atlas notebook](../notebooks/visual_intuition_atlas.ipynb) preserves the source visualization.

The next chronological article is [**Milestone 004 — Isolating the phase-aware mechanism**](./004-isolating-phase-attention.md).
