---
title: "Milestone 010 — What state should a reasoner preserve?"
description: "When is it safe for a recurrent reasoner to treat two states as equivalent?"
short_title: "What state should a reasoner preserve?"
date: 2026-09-29
authors:
  - name: Tyler J.H.G.
tags:
  - research milestone
  - executable article
---

(milestone-010)=
# Milestone 010 — What state should a reasoner preserve?
**Research period:** September 2–3, 2026  
**Historical anchors:** #193, #198, #223

One branch of the project began with a deliberately provocative question: could translating ordinary language into something more structurally explicit, such as Lojban, provide a better intermediate representation for reasoning?

That question needed an immediate correction. Tokenization, translation, and semantic normalization solve different problems. Replacing English with another serialization doesn't by itself tell us whether the representation preserves the information a reasoner will need.

The more useful question became: **when is it safe for a reasoning system to treat two internal states as equivalent?**

For a single fixed task, the answer can be straightforward. If no outcome we care about can distinguish two states, then the representation doesn't necessarily need to preserve the distinction between them. Recurrent reasoning makes that harder because today's indistinguishable states can evolve into different futures.

(010-dynamic-quotient-visual-intuition)=
## Visual intuition
```{figure} ./010_dynamic_quotient.svg
:label: 010-dynamic-quotient-intuition
:alt: A toy transition relation groups states by parity while preserving the equivalence class across steps.

Parity is a toy equivalence relation used for teaching; it is not a claim about the unpublished dynamic-quotient program.
```

## From static to dynamic sufficiency

Suppose two internal states are equivalent for the current task. If the reasoning process updates both states and they remain equivalent, then the system can continue treating them as the same. If one update sends them into states with different future behavior, the original equivalence discarded something the recurrence needed.

This means a useful compressed state for recurrent reasoning has to satisfy two requirements: it must preserve the distinctions needed for the task, and the reasoning dynamics must respect those distinctions as the state evolves.

> **Sticky note — quotient:** a quotient groups objects according to an equivalence relation and treats everything within one equivalence class as the same object for the purpose being studied. The important question is therefore not simply what gets discarded, but which distinctions we have declared irrelevant.

That shifted the target away from a particular intermediate language. I was now looking for a **dynamic or predictive quotient**: the smallest state that preserves the distinctions required for relevant future behavior.

The word *smallest* matters here conceptually, rather than as a claim that fewer dimensions are always better. Preserving every available detail is safe in one sense, but it can also make the state unnecessarily expensive and leave irrelevant variables available as shortcuts. The goal is sufficient information, rather than maximal information.

## Research context

This reframing connected the project to several older ideas that had reached similar answers from different directions.

In statistics, a **sufficient statistic** preserves the information needed for a specified inference while allowing other details of the original data to be discarded. The information bottleneck develops a related tradeoff: retain information useful for a target while compressing information that isn't useful for that target.

Sequential systems add the future-behavior requirement. **Predictive State Representations** describe state through predictions about future observable behavior rather than requiring a particular hidden-state interpretation. **Causal-state** constructions in computational mechanics similarly group histories that imply the same distribution over futures. Myhill–Nerode equivalence in automata theory and bisimulation in state-transition systems use closely related logic: two states can be merged only when the relevant future behavior cannot distinguish them.

I didn't begin the branch by combining those theories. The project arrived first at the need for a recurrence-compatible equivalence relation, and the subsequent literature sweep showed that the underlying idea had several mature precedents. Those precedents changed how I described the result: the interesting question wasn't whether I had invented a new notion of semantic state, but how these existing notions of predictive sufficiency could constrain the representation I was trying to build.

## A small editable teaching example

This six-state system illustrates a quotient under recurrence. It does not model natural-language reasoning.

Saved output is included so you can inspect the example without starting a kernel. Activating the code cell below runs this synthetic example only.

```{code-cell} python
:label: 010-dynamic-quotient-teaching-example
:tags: [illustrative, thebe]

# Toy quotient: states are equivalent if they have the same parity.
states=range(6)
R=lambda x:(x+2)%6  # respects parity
for x in states:
    print(x, 'class', x%2, '->', R(x), 'class', R(x)%2)
```

**Published teaching output (synthetic):** the saved notebook output below belongs only to the small code example. It is not a replay of historical model training.

```text
0 class 0 -> 2 class 0
1 class 1 -> 3 class 1
2 class 0 -> 4 class 0
3 class 1 -> 5 class 1
4 class 0 -> 0 class 0
5 class 1 -> 1 class 1
```


## Why Lojban stopped being the main question

A constrained language can still be useful. Lojban, AMR, DRS, UCCA, or another structured representation might provide a convenient serialization or expose relationships that ordinary text leaves implicit.

But any fixed semantic compiler has a hard boundary: if it throws away a distinction, no downstream reasoner can recover that distinction from the compiled representation alone. A representation sufficient for one declared task may therefore be insufficient for a future task that depends on something it discarded.

That made “find the right semantic language” too strong a target. A candidate language is better treated as one possible coordinate system or approximation to the state we actually care about.

The deeper target is behavioral: preserve whatever distinctions are necessary for the future reasoning and observations the system is expected to support.

## What this does not show

The dynamic-quotient formulation doesn't tell us what equivalence relation a language model should learn. Defining the correct future behavior is itself part of the modeling problem, and different tasks can require different distinctions.

It also doesn't imply that aggressive compression is always desirable. If future requirements are unknown, discarding information can permanently remove capabilities we later discover we needed. “Minimal sufficient state” only has meaning relative to a declared family of future observations, actions, or tasks.

What the formulation does give me is a test for proposed semantic representations: instead of asking whether a representation looks structured, elegant, or linguistically appealing, ask which distinctions it merges and whether those merged states remain indistinguishable under the reasoning dynamics we care about.

(010-dynamic-quotient-sources)=
## Sources and chronology
- [Milestone notebook 010 — preserved chronological source](../notebooks/010_dynamic_quotient.ipynb)
- [Research chronology](../CHRONOLOGY.md)
- [Publication dispositions and Atlas-to-article map](../PUBLICATION-DISPOSITIONS.md)

The matching Atlas theme is **Dynamic state equivalence**. The original [Visual Intuition Atlas notebook](../notebooks/visual_intuition_atlas.ipynb) remains available as a source record; this article carries the relevant static explanation inline.

The next chronological article is [**Milestone 011 — Geometry should follow invariance, not aesthetics**](./011-geometry-from-invariance.md).
