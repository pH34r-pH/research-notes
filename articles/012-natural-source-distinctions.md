---
title: "Milestone 012 — Natural-source task distinctions"
description: "Can compact states distinguish the same context leading to different futures?"
short_title: "Natural-source task distinctions"
date: 2026-09-29
model_focus: representation
depends_on: [010-dynamic-quotient]
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

The unit models occupied a compact region of their available state space. Effective rank fell, vectors became more similar, and the geometric diagnostics looked like compression. I still needed to know what had been compressed away.

Consider two representations. One discards most variation while retaining every distinction needed for a task. The other retains many dimensions but merges two cases that require different predictions. Rank and variance can describe both states, yet they cannot tell us which one supports the task.

I needed data that exposed a predictive distinction directly: **the same context leading to different futures**. Then I could test whether the compact state retained information about that distinction.

(012-natural-source-distinctions-visual-intuition)=
## Visual intuition
```{figure} ./012_natural_source_distinctions.svg
:label: 012-natural-source-distinctions-intuition
:alt: A branching example shows how longer exact contexts can become more specific while appearing less often in natural text.

A schematic branch shows the tradeoff between context specificity and repeated observations.
```

## Why Wikipedia revision history?

Two versions of a Wikipedia article can share a prefix and diverge where an editor changes the continuation. That gives us natural text with closely controlled context and different observed futures.

The revision history also preserves the source of each case. I can identify the page and revision, detect duplicates and reverts, and group related revisions when splitting or evaluating the data.

This supports a specific question: given the shared or closely controlled context, can the representation distinguish the continuations that branch in the source? We can test that prediction instead of using geometric spread as a proxy for usefulness.

## Building a benchmark that can fail

The first check is whether a constant representation fails. If every input can map to the same state and still satisfy the criterion, the benchmark has no basis for claiming that input distinctions were preserved.

I required constant and mean-state controls to fail on held-out branch cases. The protocol also compared against established sparse-context baselines, froze context lengths before qualifying evaluation, collapsed duplicates and reverts, and grouped related cases by page and revision lineage.

The grouping follows the earlier source-unit correction. Thousands of tokens from related revisions provide many measurements, but their independence still depends on the sources that produced them.

> **Sticky note — experimental unit:** the independent unit contributing evidence to a comparison. Several measurements from one source can be useful while remaining correlated.

The bounded benchmark qualified at a context length of **32 bytes**. I froze that task-distinction dataset for the next stage.

## Research context

The dynamic-sufficiency question in Milestone 010 defines a useful representation by the future distinctions it preserves. Revision branches made one such distinction observable in natural data, giving the representation an empirical target.

There is a second requirement: a prediction concerns possible outcomes, while a single recorded continuation is only one outcome. The evaluation needs to respect that difference.

> **Sticky note — proper scoring rule:** a rule for evaluating predicted probabilities whose expected score is best when we report the probabilities we actually believe. Log loss is one example.

Repeated or related branch evidence can help estimate the predictive distinction. One next token, on its own, cannot define the conditional distribution of plausible continuations.

## Try a small example

Five invented continuations show how counts become an empirical probability distribution. Change the continuations and compare the resulting probabilities.

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

The qualified benchmark provides a specific predictive distinction under a frozen natural-source protocol. I can now ask three separate questions about it: does the state retain the signal, can a small consumer recover it, and does the model's own consumer use it?

A compact state may preserve that distinction, and a larger state may lose it. Testing the distinction directly makes either outcome observable.

(012-natural-source-distinctions-sources)=
## Sources and chronology
- [Milestone notebook 012 — preserved chronological source](../notebooks/012_natural_source_distinctions.ipynb)
- [Research chronology](../CHRONOLOGY.md)
- [Publication dispositions and Atlas-to-article map](../PUBLICATION-DISPOSITIONS.md)

The matching Atlas theme is **Natural-source context support**. The earlier [Visual Intuition Atlas notebook](../notebooks/visual_intuition_atlas.ipynb) preserves the source visualization.

The next chronological article is [**Milestone 013 — Accessible does not imply used**](./accessible-does-not-imply-used.md).
