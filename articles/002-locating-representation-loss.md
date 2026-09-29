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

The first experiments told me that the spectral approach was losing performance somewhere, but an end-to-end result couldn't tell me where. To separate the possible causes, I broke the path from text to prediction into stages and tested what happened when individual stages were removed or bypassed.

`source → representation → composition → receiver → consumer → prediction`

This gave me a way to ask more specific questions: was useful information already difficult to recover from the representation itself? Did combining represented states make the problem worse? Could a learned receiver recover what composition had damaged? Or was the final language model still poorly matched to information that remained available?

> **Sticky note — control:** a comparison designed to isolate one possible explanation while keeping the other relevant conditions as similar as possible. [Reference →](../reference/glossary.md#control)

(002-locating-representation-loss-visual-intuition)=
## Visual intuition
```{figure} ./002_locating_representation_loss.svg
:label: 002-locating-representation-loss-intuition
:alt: A conceptual source-to-prediction path marks representation, composition, receiver and consumer as separately testable stages.

Conceptual stage map. Any numbers in the teaching cell below are invented to explain the accounting and are not historical measurements.
```

## Causal decomposition

The most useful comparison gave the downstream model the same source information in two forms: once as separate, uncombined components, and once after those components had been composed together. I kept the downstream model capacity matched so that differences between the two conditions would be easier to attribute to the representation pipeline itself.

The result split the original performance gap into several pieces. Some of the deficit was already present before composition, combining the components made it worse, and a learned receiver recovered part of that additional loss. No single stage explained the whole result.

That changed how I thought about the original representation problem. If some of the deficit existed before anything had been composed or recovered, then at least part of the problem could be the relationship between the representation and the model trying to use it. The information might still be present while being expressed in coordinates that make the downstream computation unnecessarily difficult.

## A small editable teaching example

The losses below are invented to show how a staged comparison works. They are not measurements from the historical experiment.

Saved output is included so you can inspect the example without starting a kernel. Activating the code cell below runs this synthetic example only.

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

**Published teaching output (synthetic):** the saved notebook output below belongs only to the small code example. It is not a replay of historical model training.

```text
pre-composition gap: 0.3999999999999999
composition penalty: 0.3999999999999999
receiver recovery: 0.19999999999999973
```


## What this does not show

Giving the model access to the uncombined components is a diagnostic control, not a proposed architecture. Its purpose is to establish whether some of the performance gap already exists before composition; in these experiments, it did.

The partial recovery from the learned receiver also has a limited interpretation. It shows that composition and recovery account for some of the deficit, but they don't explain the loss that was already present in the uncombined condition. Fixing any one stage in isolation therefore isn't guaranteed to fix the full model.

The remaining gap gave me a more specific hypothesis to test next: the downstream computation might be poorly matched to the coordinates and operations of the spectral representation itself.

(002-locating-representation-loss-sources)=
## Sources and chronology
- [Milestone notebook 002 — preserved chronological source](../notebooks/002_locating_representation_loss.ipynb)
- [Research chronology](../CHRONOLOGY.md)
- [Publication dispositions and Atlas-to-article map](../PUBLICATION-DISPOSITIONS.md)

The matching Atlas theme is **Stage-by-stage information loss**. The original [Visual Intuition Atlas notebook](../notebooks/visual_intuition_atlas.ipynb) remains available as a source record; this article carries the relevant static explanation inline.

The next chronological article is [**Milestone 003 — Coordinates matter; operations matter more**](./003-coordinates-and-matched-operations.md).
