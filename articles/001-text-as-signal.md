---
title: "Milestone 001 — What if text were a signal?"
description: "Could a signal-like representation preserve useful structure in text?"
short_title: "What if text were a signal?"
date: 2026-09-29
model_focus: tokenization
authors:
  - name: Tyler J.H.G.
tags:
  - research milestone
  - executable article
---

(milestone-001)=
# Milestone 001 — What if text were a signal?
**Research period:** earlier program, before September 1, 2026  
**Public reconstruction:** September 2026

Language models usually turn text into discrete tokens before doing anything else with it. I wanted to try treating text as a signal: give frequency and phase an explicit role in the representation, then build a model that could operate on those quantities. If useful structure was present in that form, what would the model need in order to use it?

There are two questions here. First, does the representation preserve the information? Second, can the computation recover and combine it efficiently? An invertible transformation answers the first question in principle; the second depends on the model we put around it.

> **Sticky note — representation:** the state that carries information through a model. Its usefulness depends on both the distinctions it preserves and the operations available to the next part of the model. [Reference →](../reference/representation-and-readout.md)

(001-text-as-signal-visual-intuition)=
## Visual intuition
```{figure} ./001_text_as_signal.svg
:label: 001-text-as-signal-intuition
:alt: An illustrative waveform and its frequency-coordinate view show two ways to inspect the same signal.

Toy signal: the waveform and frequency coordinates describe the same values.
```

## The first important negative result

The spectral models performed worse, even though I could recover much of the original information from their representation. That gave me a problem to locate.

Consider the path from text to prediction. The representation could lose a useful distinction when it is first constructed; combining several represented states could destroy a distinction that was initially present; or the final model could struggle to use information that remains available. An end-to-end loss measures the outcome of that whole path, so it cannot tell us which explanation is responsible.

The next experiment took the path apart. I needed to find where the information became difficult to use before deciding what to change.

## Try a small example

A toy Fourier round trip shows that the coordinate change is invertible. Try changing the input values.

```{code-cell} python
:label: 001-text-as-signal-teaching-example
:tags: [illustrative, thebe]

import numpy as np

# A tiny reminder that an invertible coordinate change need not lose information.
x = np.array([1.0, -2.0, 0.5, 3.0])
X = np.fft.fft(x)
x_roundtrip = np.fft.ifft(X).real
print('max round-trip error:', np.max(np.abs(x - x_roundtrip)))
```

**Saved output:**

```text
max round-trip error: 0.0
```


## Interpretation

Recovering the input from a representation establishes that the transformation retained it. It leaves open how much work a particular model needs to turn that representation into a useful prediction.

The worse spectral result gave the investigation a concrete target: separate the representation, the operations that combine its states, and the model that consumes them. Each stage could then be tested on its own.

(001-text-as-signal-sources)=
## Sources and chronology
- [Milestone notebook 001 — preserved chronological source](../notebooks/001_text_as_signal.ipynb)
- [Research chronology](../CHRONOLOGY.md)
- [Publication dispositions and Atlas-to-article map](../PUBLICATION-DISPOSITIONS.md)

The matching Atlas theme is **Fourier signal and frequency coordinates**. The earlier [Visual Intuition Atlas notebook](../notebooks/visual_intuition_atlas.ipynb) preserves the source visualization.

The next chronological article is [**Milestone 002 — Where did the spectral loss occur?**](./002-locating-representation-loss.md).
