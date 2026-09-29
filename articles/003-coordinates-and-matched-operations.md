---
title: "Milestone 003 — Coordinates matter; operations matter more"
description: "Does changing coordinates help, or do the operations need to change too?"
short_title: "Coordinates matter; operations matter more"
date: 2026-09-29
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

The previous experiment left open the possibility that the spectral representation wasn't inherently deficient; the downstream model might simply have been doing the wrong kind of computation on it. I tested that by holding the uncombined spectral state fixed and changing only how the downstream model represented and processed the same information.

There were two changes I needed to separate. Rewriting a complex value from Cartesian coordinates into `[rho, cos(theta), sin(theta)]` might make the information easier for a model to use even if the computation itself stayed essentially the same. Alternatively, operations designed around magnitude and phase might provide an additional advantage. A coordinate-only control let me measure those effects separately.

> **Sticky note — log-polar:** a complex value can be described by its magnitude and phase. `rho = log(|z| + eps)` represents magnitude on a logarithmic scale, while `theta` represents its angle.

(003-coordinates-and-matched-operations-visual-intuition)=
## Visual intuition
```{figure} ./003_coordinates_and_matched_operations.svg
:label: 003-coordinates-and-matched-operations-intuition
:alt: A conceptual complex-plane diagram separates coordinate re-expression from changing the downstream operation.

Toy complex values can be re-expressed in polar coordinates. Changing the operation is a separate choice.
```

## Result

Both changes helped, but by different amounts. Rewriting the spectral state into the coordinate-only representation improved the result, showing that coordinates alone affected how easily the downstream model could use the information. The polar-native processing path improved loss substantially further.

Compared with the original spectral Cartesian condition, the polar-native model improved loss by about **0.5825 nat per original byte**. More importantly, it improved loss by about **0.3923 nat per original byte** compared with the coordinate-only control containing the same underlying information. All three experimental seeds cleared the predefined materiality threshold.

That second comparison changed the interpretation of the experiment. A coordinate transformation could explain part of the original improvement, but it couldn't explain all of it. Something about the operations performed in those coordinates was contributing independently.

## Try a small example

Three hand-chosen complex values show how Cartesian and polar coordinates describe the same information. The saved output below is available without starting Python.

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

The coordinate-only control separated the benefit of re-expression from the benefit of the polar-native block. Several operations inside that block still changed together. The next experiment therefore took the block apart while holding the source representation fixed, to find which operation carried the remaining advantage.

(003-coordinates-and-matched-operations-sources)=
## Sources and chronology
- [Milestone notebook 003 — preserved chronological source](../notebooks/003_coordinates_and_matched_operations.ipynb)
- [Research chronology](../CHRONOLOGY.md)
- [Publication dispositions and Atlas-to-article map](../PUBLICATION-DISPOSITIONS.md)

The matching Atlas theme is **Phase-aware coordinates**. The original [Visual Intuition Atlas notebook](../notebooks/visual_intuition_atlas.ipynb) remains available as a source record; this article carries the relevant static explanation inline.

The next chronological article is [**Milestone 004 — Isolating the phase-aware mechanism**](./004-isolating-phase-attention.md).
