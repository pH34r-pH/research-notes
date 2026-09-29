---
title: "Milestone 001 — What if text were a signal?"
description: "Could a signal-like representation preserve useful structure in text?"
short_title: "What if text were a signal?"
date: 2026-09-29
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

Language models usually begin by converting text into discrete tokens, but that isn't the only way text can be represented. I wanted to see what would happen if we instead treated text more literally as a signal: could frequency, phase, or oscillator-like representations preserve useful structure, and could a language model learn to use it?

The initial hypothesis was intentionally broad. If text contains regularities that are easier to express in a signal-like representation, a model designed to operate on that representation might be able to take advantage of them.

> **Sticky note — representation:** the state used to carry information forward through a model. Whether a representation is useful depends on what information it preserves and what the next part of the model can actually recover from it. [Reference →](../reference/representation-and-readout.md)

(001-text-as-signal-visual-intuition)=
## Visual intuition
```{figure} ./001_text_as_signal.svg
:label: 001-text-as-signal-intuition
:alt: An illustrative waveform and its frequency-coordinate view show two ways to inspect the same signal.

Toy signal: the waveform and frequency coordinates describe the same values.
```

## The first important negative result

The early experiments didn't show a clear advantage for the spectral representation. I could recover much of the original information from it, but language models using that representation still performed worse.

That result was more interesting than a simple failure because it left several possible explanations open. The representation itself might have lost something important; the operations used to combine represented text might have destroyed distinctions that were initially present; or the downstream model might simply have been poorly suited to reading the resulting state.

This changed the question from “does spectral text work?” to “where does the information become unusable?” That became the focus of the next phase.

## Try a small example

A toy Fourier round trip shows that the coordinate change is invertible. Try changing the input values. The saved output below is available without starting Python.

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

An invertible coordinate change preserves information, but the model still has to use it. The spectral model’s worse performance left three places to investigate: the representation, the operations that combined represented states, and the downstream consumer. Keeping the negative result gave the next experiment a specific job: locate the loss.

(001-text-as-signal-sources)=
## Sources and chronology
- [Milestone notebook 001 — preserved chronological source](../notebooks/001_text_as_signal.ipynb)
- [Research chronology](../CHRONOLOGY.md)
- [Publication dispositions and Atlas-to-article map](../PUBLICATION-DISPOSITIONS.md)

The matching Atlas theme is **Fourier signal and frequency coordinates**. The original [Visual Intuition Atlas notebook](../notebooks/visual_intuition_atlas.ipynb) remains available as a source record; this article carries the relevant static explanation inline.

The next chronological article is [**Milestone 002 — Where did the spectral loss occur?**](./002-locating-representation-loss.md).
