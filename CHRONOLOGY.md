# Research chronology manifest

This manifest reconstructs the public research narrative from the private execution record and the human-readable Notion chronology. Dates below describe the **research period**, not the Git commit date of the reconstructed public note.

The reconstruction rule is: **question → experiment/derivation → boundary → later controls/literature → narrowed next question**. Retrospective notes may mention later evidence when needed to prevent an earlier result from being misleading, but they must label that perspective explicitly.

| # | Research period | Public note | Historical anchors | Public purpose | Formal support | Disclosure |
|---|---|---|---|---|---|---|
| 001 | Earlier program, pre-2026-09-01 | What if text were a signal? | #71–#120; Gate A | Establish representation as an experimental variable and explain why spectral text was revised rather than declared successful | none required | public synthesis; synthetic examples only |
| 002 | Earlier program | Where did the spectral loss occur? | #121–#123 | Separate representation quality, composition loss, receiver recovery, and downstream geometry | none required | public causal decomposition; omit private artifacts |
| 003 | 2026-09-01 | Coordinates matter; operations matter more | #161–#162 | Introduce controlled coordinate reparameterization and the first positive co-design result | none required | publish stable aggregate contrasts already recorded in chronology |
| 004 | 2026-09-01 | Isolating the phase-aware mechanism | #163 | Show why operation ablation narrowed the positive result to phase/Hermitian Q/K similarity | none required | publish bounded mechanism classification |
| 005 | 2026-09-01→02 | The unit-hypersphere anomaly | #164 | Present the surprising frozen endpoint and retained-radius comparison without treating it as final mechanism identification | later LIB-SPH-002 context | publish historical aggregate endpoints |
| 006 | 2026-09-02→05 | A dramatic endpoint can still mislead | #176, #177, #211 | Show trajectory, regularization, stopping-policy, cost, and source-unit corrections that weakened the simple sphere story | formal boundaries only | publish stable classifications/aggregates; emphasize retrospective correction |
| 007 | 2026-09-02→03 | Derive before training | #196, #199, #200, #252 | Explain normalization's radial/tangent derivative and why formalization became useful for pruning interpretations | LIB-SPH-002 / FRM-000020 | public theorem link; no private ledger state |
| 008 | 2026-09-03→05 | What does the sphere actually do? | #201–#206 | Synthesize frozen interventions, Jacobians, cocycles, sensitivity, probes, and the decision not to launch unnecessary training | LIB-SPH-002 and related public core where available | classifications only; no active frontier |
| 009 | 2026-09-03 | From hypothesis sprawl to theorem ledger | #196, #198–#200, later #257 | Explain proof-first architecture selection and epistemic status separation | theorem-library infrastructure | public methodology; private ledger remains authoritative |
| 010 | 2026-09-02→03 | What state should a reasoner preserve? | #193, #198, #223 | Semantic compiler → sufficient state → dynamic quotient/predictive state | dynamic-quotient theorem remains private until classified PUBLIC-CORE | educational derivation; no unpublished empirical claim |
| 011 | 2026-09-02→03 | Geometry should follow invariance | #194–#198 | Radius/structure, product vs warped geometry, Grassmann, operator algebra, mixed geometry; demonstrate proof-driven pruning | link public formal results only when exported | synthesis; no claim of novelty for established primitives |
| 012 | 2026-09-03 onward | Natural-source task distinctions | #178–#180, #316, #318, #323, #325 | Explain why aggregate loss/rank was insufficient and why revision branches became a task-aligned natural-source gate | theorem boundaries as relevant | publish protocol logic and qualified stable result only |
| 013 | 2026-09-08→09 | Accessible does not imply used | #328 | Affine probing, selectivity, MDL, accessibility vs native utilization | representation/readout reference | publish stable accessible-but-underused result |
| 014 | current/future | Can a tiny consumer use what the state knows? | #331 | Readout-utilization ladder on the actual 256-way prediction task | TBD | hold until stable milestone |

## Editorial rules for reconstructed notes

1. Each notebook states **Research period** and **Public reconstruction date** separately.
2. Git history is never rewritten to simulate historical publication.
3. Historical positive results are followed by later corrections when omission would leave a materially false impression.
4. A notebook distinguishes `✓ Formal checkpoint`, `● Observation`, `◇ Assumption`, and `? Hypothesis`.
5. Every notebook contains **What this does not show** and **Understanding questions**.
6. Runnable code is a synthetic teaching example unless a public artifact is explicitly identified as an exact replay.
7. Private experiment artifacts, exact active queues, unpublished hypotheses, and theorem-ledger lifecycle state remain private.
8. Literature discovered after an internal derivation is described as later convergence/prior-art context, never as evidence of novelty.
## Current edge

The immediate next question follows directly from Milestone 013: if useful information is accessible in the frozen state but the native consumer underuses it, **how small can a replacement consumer be while still converting that information into better predictions on the actual next-byte task?**

That experiment is active. It will become the next numbered milestone only after the result and its interpretation are stable.

Beyond that experiment, the current research sequence is dependency-driven rather than preassigned to notebook numbers:

1. establish the bounded next-byte readout result;
2. prove the shared-subspace and functional-sufficiency boundaries that can be settled mathematically before another experiment;
3. establish a reproducible baseline for the historical hypersphere experiment using existing standards and a clean execution environment;
4. use that baseline for controlled optimizer comparisons;
5. return to approximate shared-subspace questions with the theorem-derived burden removed;
6. apply the resulting representation → accessibility → utilization → causal-function framework to external methodology replications where useful.

Infrastructure work can proceed in parallel when it unblocks those questions, but infrastructure completion by itself does not create a research milestone.

## Planning future milestones

A notebook represents a stable change in what I think the evidence supports, rather than the completion of a GitHub issue. One notebook may synthesize several issues, and many infrastructure or documentation issues should never become notebooks.

The publication path is:

`active question → stable result → interpretation review → public theorem promotion where applicable → notebook → portfolio publication`

This keeps the public chronology tied to research conclusions while allowing the implementation plan underneath it to change.

## Reconstruction rules

The public notebooks follow a few simple rules:

- Keep results in the order they were discovered, including results that were later reinterpreted.
- Make later corrections visible when leaving them out would make an earlier result misleading.
- Distinguish mathematical results from empirical observations and from the interpretations built on either.
- Treat runnable examples as synthetic unless they're explicitly identified as reproductions of historical data.
- When literature was found after an internal result, describe the relationship as later convergence or prior-art context rather than rewriting the paper as the original inspiration.
- Explain enough of a referenced idea that following the link is optional for understanding the notebook.

The purpose of the chronology is to preserve how the research changed, including the dead ends and corrections that determined what became worth asking next.
