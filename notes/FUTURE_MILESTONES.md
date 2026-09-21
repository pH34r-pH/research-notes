# Future milestone planning

This file tracks likely public research directions without reserving notebook numbers or treating issue completion as publication.

## Current sequence

| Order | Research question | Primary work | Publication condition |
|---|---|---|---|
| 1 | Can a small readout recover useful next-byte prediction from the frozen state? | domain-scaling-lab #331 | A bounded consumer-ladder classification is stable and controls are complete. |
| 2 | What does low-rank/shared-subspace geometry actually imply? | domain-scaling-lab #338, supported by #341 | Proof targets are checked, discovery/prior-art audit is complete, and reusable results are promoted where appropriate. |
| 3 | Can the historical #164 experiment be reproduced from a portable scientific description? | domain-scaling-lab #342/#344 + long-haul-fleet #19 | Baseline encoding, clean replay, provenance, and conceptual-reproduction boundary are stable. |
| 4 | Does Muon improve useful training efficiency in this small regime? | domain-scaling-lab #343 | AdamW reproducibility gate passes and the optimizer treatment is frozen before qualifying runs. |
| 5 | Is there an approximate shared active subspace that transfers and aligns with function? | empirical follow-up to #338 | Held-out shared-plane evidence survives common-mode and functional-alignment controls. |
| 6 | How far does the representation → intervention → behavior ladder carry under an external methodology? | domain-scaling-lab #346 | Replication/control results are stable and interpreted within the formal sufficiency boundaries. |

## Parallel enabling work

Long Haul and long-haul-fleet provide execution and physical-vessel infrastructure. MCP identity/authorization, Kestrel qualification, and the disposable reference-vessel protocol can progress in parallel when they unblock the research sequence.

Formal discovery infrastructure (#341) is similarly enabling work: it should improve proof search and novelty auditing, but becomes part of the public research narrative only when it changes a scientific conclusion or method worth explaining.

## Publication rule

A future notebook should answer all four questions:

1. What question changed?
2. What evidence settled or narrowed it?
3. What interpretation is justified, and what remains outside the evidence?
4. What became rational to do next?

If closing an issue does not change any of those answers, it probably does not need a notebook.
