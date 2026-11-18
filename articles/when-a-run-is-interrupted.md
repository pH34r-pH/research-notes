---
title: "When a run is interrupted, what can the record still tell us?"
description: "How attempt receipts and container journals preserve evidence after an interrupted experiment."
short_title: "When a run is interrupted, what can the record still tell us?"
date: 2026-11-01
article_kind: essay
authors:
  - name: Tyler J.H.G.
tags:
  - research infrastructure
---

# When a run is interrupted, what can the record still tell us?

One of the less interesting-looking problems in experiment infrastructure is what happens when the thing controlling a run stops before the run finishes. The obvious answer is that the experiment didn't complete, but even that can be more complicated: the controller may have stopped while a container it started is still running, or the workload may have finished without the controller recording a final result.

For Experiment Compiler, I want the attempt record to make those cases distinguishable. A receipt saying that a run started is evidence that the controller started an attempt; it isn't evidence that the scientific work finished. Similarly, cleaning up a leftover container is an operational result, not a scientific result.


```{figure} ./interrupted-run.svg
:alt: An attempt receipt and container journal help recovery preserve uncertainty after a controller interruption.

An attempt receipt and container journal help recovery preserve uncertainty after a controller interruption.
```

## What gets recorded?

The runner writes an attempt receipt before launching the workload. If the attempt reaches a terminal state, the receipt records that outcome; if it remains marked as started, the attempt is incomplete. The runner also keeps bounded logs and, where available, cancellation and cleanup diagnostics.

This matters because otherwise an interruption can get confused with either success or a negative scientific result. Suppose an experiment is interrupted before it produces an output. We haven't observed the experiment succeed, but we also haven't observed evidence against the hypothesis it was meant to test. The thing we know is that the attempt was interrupted or remains unresolved.

## What happens to the containers?

After a controller is lost, recovery needs to identify the specific containers that belonged to the attempt. A broad name search isn't enough, because another process could have started a similarly named container. The runner keeps a container-identity journal alongside the attempt, and its recovery command can reconcile the recorded identities without rerunning the workflow.

The identity problem applies to process IDs as well. IDs can be reused, so an old numeric ID alone isn't sufficient reason to signal a process after a restart. If the kernel boot ID has changed, the old process group can't still exist; if the environment restarted without a different kernel boot ID, the situation can remain ambiguous. When the journal is stale or identity can't be established, recovery fails closed instead of guessing.

The receipt binds the private journal by digest. A result ZIP can expose the journal digest and a sanitized cleanup summary while leaving host-specific operational details in the private attempt store. That makes it possible to connect the result to the cleanup record without putting every local detail into the distributable package.

## What does that prove?

These mechanisms improve the record of what the controller observed and what cleanup it could verify. They don't prove that the scientific workload completed, that its results passed the protocol's checks, or that the environment enforced every isolation boundary. In particular, the hermetic tests of this behavior don't by themselves establish physical worker-loss recovery or production-worker qualification.

The goal is to retain enough information to tell what happened, and to leave the uncertain cases visibly uncertain. An incomplete attempt is still part of the history of the experiment; it just shouldn't be promoted into a result that nobody observed.

**Sources:** [Lifecycle and runner documentation](https://github.com/pH34r-pH/experiment-compiler/blob/f47ac10a8f9b954911518e823bc6a35df06041e7/docs/wiki/Lifecycle-and-Runner.md); [Experiment Compiler overview](https://github.com/pH34r-pH/experiment-compiler/blob/f47ac10a8f9b954911518e823bc6a35df06041e7/README.md).
