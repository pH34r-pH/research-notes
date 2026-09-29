---
title: "Milestone 006 — A dramatic endpoint can still mislead"
description: "Does an apparent advantage survive fair checkpoint selection?"
short_title: "A dramatic endpoint can still mislead"
date: 2026-09-29
authors:
  - name: Tyler J.H.G.
tags:
  - research milestone
  - executable article
---

(milestone-006)=
# Milestone 006 — A dramatic endpoint can still mislead
**Research period:** September 2–5, 2026  
**Historical anchors:** #176, #177, #211

The unit-hypersphere result in the previous notebook was real: at the frozen 128-update endpoint, that model performed dramatically better than the alternatives. What changed afterward was the explanation.

I kept investigating the anomaly instead of treating the endpoint as confirmation of a hyperspherical advantage. Longer training, stronger controls, and a fair checkpoint-selection policy eventually showed that the original result could be explained without requiring a geometry-specific effect.

This notebook is therefore retrospective. The earlier measurement remains part of the record; the conclusions I was willing to draw from it changed as better evidence became available.

(006-endpoint-can-mislead-visual-intuition)=
## Visual intuition
```{figure} ./006_endpoint_can_mislead.svg
:label: 006-endpoint-can-mislead-intuition
:alt: Schematic learning curves illustrate that the best checkpoint and a fixed late checkpoint can rank conditions differently.

Schematic curves only; the historical comparison and its corrections are described in the source note below.
```

## What changed

The first problem was the **training trajectory**. Extending the experiments showed that the models were following different learning curves and reaching their strongest observed results at different times. The shared and retained-radius models reached much better losses earlier, while the unit model's apparent advantage emerged later. Comparing all of them at one late checkpoint had therefore emphasized one particular part of those trajectories.

The second problem was **regularization**. A Cartesian control designed to reproduce the unit model's effects on vector norms and rank came close enough to the original improvement that the frozen decision rule returned **REGULARIZATION-EXPLAINS**. This didn't prove that geometry was irrelevant, but it removed the need for geometry to explain the original endpoint anomaly: an ordinary representation with comparable regularization could reproduce the effect.

The third problem was **checkpoint selection**. I froze a common selection policy before comparing the models so that each architecture would be judged by the same rule rather than by whichever checkpoint happened to make it look best.

Under that policy, selected validation NLL per byte was:

- shared recurrence: **3.3760**
- retained-radius recurrence: **3.3768**
- unit-hypersphere recurrence: **3.6205**

Lower is better. The unit model was therefore about **0.2445 nat per byte worse** than the shared model, with the simultaneous 95% interval entirely above zero. It also consumed about **3.44×** the mean training-plus-selection dense-operation budget.

The comparison had reversed. The same model that looked dramatically better at the original frozen endpoint was worse under the later fair-selection comparison, and substantially more expensive to reach that comparison.

> **Sticky note — checkpoint selection:** training produces many intermediate versions of a model. A selection policy specifies which checkpoint will be used for comparison. If that rule is chosen after looking at the results, checkpoint choice can quietly become another tuned hyperparameter.

There was also a statistical correction. An audit of the historical data showed that some rows I had previously treated as separate observations did not correspond to independent source articles. That matters because repeated measurements from the same underlying source don't provide as much independent evidence as measurements from genuinely separate sources.

> **Sticky note — independent sampling unit:** the unit that contributes genuinely independent evidence to an analysis. Counting correlated measurements as independent observations makes uncertainty look smaller than it really is.

## A small editable teaching example

These short loss sequences are invented to illustrate checkpoint selection. They are not the historical training curves.

Saved output is included so you can inspect the example without starting a kernel. Activating the code cell below runs this synthetic example only.

```{code-cell} python
:label: 006-endpoint-can-mislead-teaching-example
:tags: [illustrative, thebe]

# Why selection policy matters: the best checkpoint and a fixed late checkpoint can rank models differently.
shared = [3.9, 3.0, 3.4]
unit = [4.1, 3.5, 3.2]
print('best shared/unit:', min(shared), min(unit))
print('late shared/unit:', shared[-1], unit[-1])
```

**Published teaching output (synthetic):** the saved notebook output below belongs only to the small code example. It is not a replay of historical model training.

```text
best shared/unit: 3.0 3.2
late shared/unit: 3.4 3.2
```


## What this does not show

None of this makes the original endpoint measurement wrong. A fixed endpoint, the best checkpoint observed during training, and a checkpoint selected under a predefined policy are different measurements answering different questions. The mistake would be treating one of them as interchangeable with the others.

Likewise, **REGULARIZATION-EXPLAINS** doesn't establish that hyperspherical geometry can never matter. It says that I didn't need a geometry-specific explanation for the result that originally motivated the investigation; a matched regularization control was sufficient to account for it under the frozen decision rule.

For me, the more important result was methodological. A surprising measurement should create more opportunities to prove the first explanation wrong. In this case, the anomaly survived long enough to motivate better trajectory analysis, regularization controls, checkpoint-selection rules, and source-unit auditing; those controls produced a much less dramatic explanation, and a much stronger result.

(006-endpoint-can-mislead-sources)=
## Sources and chronology
- [Milestone notebook 006 — preserved chronological source](../notebooks/006_endpoint_can_mislead.ipynb)
- [Research chronology](../CHRONOLOGY.md)
- [Publication dispositions and Atlas-to-article map](../PUBLICATION-DISPOSITIONS.md)

The matching Atlas theme is **Checkpoint trajectories**. The original [Visual Intuition Atlas notebook](../notebooks/visual_intuition_atlas.ipynb) remains available as a source record; this article carries the relevant static explanation inline.

The next chronological article is [**Milestone 007 — Derive before training**](./007-derive-before-training.md).
