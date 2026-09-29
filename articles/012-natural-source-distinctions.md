---
title: "Milestone 012 — Natural-source task distinctions"
description: "Can compact states distinguish the same context leading to different futures?"
short_title: "Natural-source task distinctions"
date: 2026-09-29
authors:
  - name: Tyler J.H.G.
tags:
  - research milestone
  - executable article
---

(milestone-012)=
# Milestone 012 — Natural-source task distinctions
**Research period:** September 2026  
**Historical anchors:** #178–#180, #316, #318, #323, #325

The unit-hypersphere models produced very compact internal states. Effective rank fell, vectors became more similar to one another, and several geometric diagnostics suggested that the representation was occupying a much smaller region of its available space.

That looked like compression, but compression alone wasn't enough to tell me whether anything useful had been lost.

A representation can discard enormous amounts of variation while preserving everything a particular task needs. It can also retain plenty of geometric variation while losing one distinction that matters. Effective rank, variance, cosine similarity, and similar summaries describe the state; they don't tell us whether two situations that require different predictions are still distinguishable.

I needed a benchmark where the data itself provided examples of **the same context leading to meaningfully different futures**.

(012-natural-source-distinctions-visual-intuition)=
## Visual intuition
```{figure} ./012_natural_source_distinctions.svg
:label: 012-natural-source-distinctions-intuition
:alt: A branching example shows how longer exact contexts can become more specific while appearing less often in natural text.

A schematic branch shows the tradeoff between context specificity and repeated observations.
```

## Why Wikipedia revision history?

Wikipedia revisions provide naturally occurring branch points. Two versions of an article can share a prefix and then diverge because an editor changed what came next. That gives us real text, written for reasons unrelated to the experiment, where closely related contexts can lead to different continuations.

The revision history also preserves provenance. I can identify which page and revision produced an example, detect reverts and duplicates, and keep related revisions together when splitting or evaluating the data.

That made revision branches useful for a task-aligned question:

**given a shared or closely controlled context, does the representation preserve enough information to distinguish futures that the source data shows are genuinely different?**

This is different from measuring how many dimensions the representation occupies. The benchmark only cares about distinctions that affect the predictive task.

## Building a benchmark that can fail

A benchmark like this needs a negative control. If a representation that maps every input to the same constant state can satisfy the criterion, then the criterion isn't measuring preserved distinctions at all.

The protocol therefore required constant and mean-state controls to fail on held-out branch cases. It also compared against established sparse-context baselines, froze the context lengths before qualifying evaluation, collapsed duplicates and reverts, and grouped related examples by page and revision lineage.

Those grouping rules became especially important after the earlier source-unit audit. Thousands of tokens extracted from closely related revisions don't become thousands of independent pieces of evidence just because they occupy different rows in a dataset.

> **Sticky note — experimental unit:** the independent unit that contributes evidence to a statistical comparison. Multiple measurements from the same underlying source can be useful, but treating them as independent makes the evidence appear stronger than it is.

The bounded natural-source benchmark eventually qualified at a context length of **32 bytes**. That became the frozen task-distinction dataset used in the next stage of the investigation.

## Research context

This benchmark design followed directly from the dynamic-sufficiency question in Notebook 010. If a useful representation is defined by the distinctions it preserves for future behavior, then evaluating representation quality requires examples where those future distinctions are observable.

Revision histories offered a practical natural-source approximation to that idea. Instead of inventing synthetic labels for “semantic difference,” I could use real branch points and ask whether a representation retained information relevant to their different continuations.

The statistical side of the design also drew on a much older principle: predictions should be evaluated against the distribution of possible outcomes rather than only the one outcome that happened to be observed in a particular sample.

> **Sticky note — proper scoring rule:** a scoring rule evaluates predicted probabilities. A *proper* scoring rule is designed so that, on average, the best strategy is to report the probabilities you actually believe. Log loss, which this project uses extensively, is one example.

That matters for branch data because one realized continuation isn't the same thing as the conditional distribution of plausible continuations. The benchmark needs enough repeated or related evidence to estimate the distinction without pretending that one observed next token defines the entire predictive problem.

## Try a small example

Five invented continuations show how to form an empirical distribution and calculate its entropy. The saved output below is available without starting Python.

```{code-cell} python
:label: 012-natural-source-distinctions-teaching-example
:tags: [illustrative, thebe]

from collections import Counter
continuations = [b'a',b'a',b'b',b'a',b'b']
counts=Counter(continuations); n=sum(counts.values())
print({k.decode():v/n for k,v in counts.items()})
# A branch needs multiple supported continuations; one realized token is not a conditional distribution.
```

**Saved output:**

```text
{'a': 0.6, 'b': 0.4}
```


## Interpretation

The qualified benchmark supplies a specific natural-source predictive distinction under a frozen protocol. Representation quality can now be tested against that distinction: whether the signal remains present, whether a small readout recovers it, and whether the native model uses it.

Effective rank and compression alone cannot answer those questions. A compact representation can preserve the task’s required distinctions, while a larger one can still lose them.

(012-natural-source-distinctions-sources)=
## Sources and chronology
- [Milestone notebook 012 — preserved chronological source](../notebooks/012_natural_source_distinctions.ipynb)
- [Research chronology](../CHRONOLOGY.md)
- [Publication dispositions and Atlas-to-article map](../PUBLICATION-DISPOSITIONS.md)

The matching Atlas theme is **Natural-source context support**. The original [Visual Intuition Atlas notebook](../notebooks/visual_intuition_atlas.ipynb) remains available as a source record; this article carries the relevant static explanation inline.

The next chronological article is [**Milestone 013 — Accessible does not imply used**](./accessible-does-not-imply-used.md).
