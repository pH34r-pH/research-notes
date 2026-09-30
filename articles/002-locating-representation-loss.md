---
title: "Milestone 002 — Where did the spectral loss occur?"
description: "Where between representation and prediction does useful information become hard to recover?"
short_title: "Where did the spectral loss occur?"
date: 2026-09-29
authors:
  - name: Tyler J.H.G.
tags:
  - research milestone
  - executable article
---

(milestone-002)=
# Milestone 002 — Where did the spectral loss occur?
**Research period:** earlier program  
**Historical anchor:** #123

The spectral model had a performance gap, and I needed to know where it came from. I split the computation into stages, then removed or bypassed individual stages while keeping the rest of the comparison matched.

`source → representation → composition → receiver → consumer → prediction`

Suppose the consumer receives the original represented components separately. If performance is already worse at that point, composition cannot explain the whole gap. If combining those components makes performance worse again, composition introduces an additional problem. A learned receiver then gives us a third comparison: how much of that additional loss can it recover?

> **Sticky note — control:** a comparison that isolates one possible explanation by keeping the other relevant conditions as similar as possible. [Reference →](../reference/glossary.md#control)

(002-locating-representation-loss-visual-intuition)=
## Visual intuition
```{figure} ./002_locating_representation_loss.svg
:label: 002-locating-representation-loss-intuition
:alt: A conceptual source-to-prediction path marks representation, composition, receiver and consumer as separately testable stages.

A stage map separates representation, composition, recovery, and prediction.
```

## Causal decomposition

I gave models with matched downstream capacity the same source information in two forms: separate components, and the state produced by composing those components. This made the representation pipeline the main difference between the conditions.

Some of the performance deficit was present before composition. Composing the components added more loss, and a learned receiver recovered part of that addition. The original gap therefore contained several problems, with different places to intervene.

The pre-composition deficit was particularly useful. It meant that changing composition alone would leave part of the problem in place. I needed to examine how the consumer operated on the spectral state: were its coordinates and operations making available information unnecessarily difficult to use?

## Try a small example

A toy comparison with invented losses shows how to separate the gap at each stage.

```{code-cell} python
:label: 002-locating-representation-loss-teaching-example
:tags: [illustrative, thebe]

# Synthetic loss accounting: the numbers are illustrative, not historical replay.
byte = 2.0
uncomposed = 2.4
composite = 2.8
recovered = 2.6
print('pre-composition gap:', uncomposed-byte)
print('composition penalty:', composite-uncomposed)
print('receiver recovery:', composite-recovered)
```

**Saved output:**

```text
pre-composition gap: 0.3999999999999999
composition penalty: 0.3999999999999999
receiver recovery: 0.19999999999999973
```


## Interpretation

The separate-component control exposed a gap before composition, while the receiver recovered part of the extra loss after composition. Those comparisons gave me two effects to investigate independently.

I started with the first: hold the spectral information fixed and change the computation that consumes it. That would test whether the mismatch lay in the representation itself or in how the model processed it.

(002-locating-representation-loss-sources)=
## Sources and chronology
- [Milestone notebook 002 — preserved chronological source](../notebooks/002_locating_representation_loss.ipynb)
- [Research chronology](../CHRONOLOGY.md)
- [Publication dispositions and Atlas-to-article map](../PUBLICATION-DISPOSITIONS.md)

The matching Atlas theme is **Stage-by-stage information loss**. The earlier [Visual Intuition Atlas notebook](../notebooks/visual_intuition_atlas.ipynb) preserves the source visualization.

The next chronological article is [**Milestone 003 — Coordinates matter; operations matter more**](./003-coordinates-and-matched-operations.md).
