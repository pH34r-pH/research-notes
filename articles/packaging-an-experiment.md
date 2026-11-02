---
title: "What does it mean to package an experiment?"
description: "How Experiment Compiler preserves reviewed inputs, execution records, and scientific interpretation."
short_title: "What does it mean to package an experiment?"
date: 2026-11-01
article_kind: essay
authors:
  - name: Tyler J.H.G.
tags:
  - research infrastructure
---

# What does it mean to package an experiment?

I've been working on a tool called Experiment Compiler, which is meant to make an experiment into a portable, inspectable package. The basic idea is fairly simple: instead of giving someone a repository and saying “run this,” give them a versioned artifact that identifies the code, inputs, procedure, and environment that make up the experiment.

There are a few complications with that, though. For example, if I give you a package and you verify that all of its files match the manifest, you know that the package is internally consistent. You don't necessarily know that it's the package I intended to give you; for that, you need an independently supplied identity, like an expected digest. And even if it is the right package, verifying the files doesn't tell you whether the experiment was ever run.

That distinction is important because I want someone to be able to answer several different questions: what was planned, what was actually executed, what did it produce, and what interpretation did the researcher put on the result? Those are connected, but they don't all have the same evidence behind them.


```{figure} ./packaging-an-experiment.svg
:alt: The package, the run, and the interpretation answer different questions.

The package, the run, and the interpretation answer different questions.
```

## The package and the run

Experiment Compiler takes reviewed inputs and assembles them into a versioned artifact with an inventory, provenance, and declared dependencies. Where possible, it uses existing standards such as RO-Crate and CWL to describe those relationships. The intent is that someone inspecting the package can find the relevant files and understand what the workflow expects without relying on a particular hosted service.

The compiler can verify that the artifact matches its declared contents. A separately supplied digest can identify a specific expected artifact. Neither check establishes that the scientific procedure succeeded; they establish properties of the package.

Execution is a separate step. The runner records an attempt, including its outcome and available logs, and the source can then attach an interpretation to the retained result. A successful process exit tells us the execution completed according to that record. It doesn't tell us whether the experiment was well designed or whether the result supports the interpretation.

Why separate all of this? Because the failure cases are different. If the package is missing an input, the first problem is that it can't be run as specified. If it runs but the result doesn't meet the acceptance criteria, that's a different result. And if the measurements are valid but the comparison isn't appropriate, the scientific interpretation is still open. Treating all three as a single pass/fail status would hide the part we actually need to investigate.

## The Muon example

The first real-study walkthrough uses a comparison involving the unit-hypersphere model from the earlier research. The treatment applied Muon to selected matrix weights and AdamW to the remaining parameters, then compared the resulting trajectories with a historical AdamW reference. The treatment was run for three seeds; the reference was retained from the earlier experiment rather than being run again as a fresh control.

The result was mixed. The primary trajectory measure favored the historical AdamW reference, while the secondary final measurement favored Muon. The source's interpretation is inconclusive; it doesn't claim that one optimizer is generally better.

There is also an unresolved compatibility issue. The treatment and historical controls have matching initial-state fingerprints and source-document identities, but their retained data-representation fingerprints differ. Recalculating the reported result from the retained data can check the arithmetic, but it doesn't establish that those representations are compatible for a causal optimizer comparison.

This is exactly the kind of result I want the package to be able to preserve. The plan, attempt, selected observations, and source interpretation can all be inspected, including the parts that limit the conclusion. A package doesn't need to produce a positive result to be useful.

## Reproduction is another question

The public artifact can be rebuilt and verified without running the scientific workload. That checks the retained package; it isn't an independent reproduction of the experiment. To reproduce it, someone would need the appropriate inputs and runtime, an acceptable comparison, and an independently observed run, followed by evaluation under the protocol.

The compiler doesn't decide whether the question is worth asking or whether the conclusion is correct. What it can do is make the evidence for each stage easier to find and check, including when the result is incomplete or inconclusive.

**Sources:** [Experiment Compiler](https://github.com/pH34r-pH/experiment-compiler/blob/f47ac10a8f9b954911518e823bc6a35df06041e7/README.md); [real-study walkthrough](https://github.com/pH34r-pH/experiment-compiler/blob/f47ac10a8f9b954911518e823bc6a35df06041e7/docs/real-study-walkthrough.md); [public experiment record](https://experiments.tyharbin.com/experiments/muon-unit-hypersphere-depth3-multiseed-v1-final-87409154/).
