# Editorial Guide

These notes should feel like a good technical textbook that happens to follow a live research program.

## Two layers

### Milestone notebooks

The notebooks are the narrative spine. They should be readable in chronological order and answer:

1. What question were we trying to answer?
2. Why did the answer matter?
3. What competing explanations were still possible?
4. What experiment separated them?
5. What did we observe?
6. What are we justified in concluding?
7. What does the result *not* establish?
8. How did the result change the next question?

### Reference material

The `reference/` tree is the reusable textbook layer. It should explain concepts independently of any single milestone and provide stable targets for links from notebooks.

Do not duplicate long explanations inside notebooks. Use a sticky note locally, then link to the deeper reference treatment.

## Sticky notes

A sticky note defines one component of a dense technical statement in one or two sentences. It should be useful even to a reader who last took the relevant class years ago.

Example:

> **Sticky note — affine:** An affine map is a linear transformation plus a bias: `z = Wx + b`. It can rotate, rescale, mix, and shift coordinates, but it cannot create nonlinear feature interactions by itself. [Deeper reference →](../reference/glossary.md#affine-map)

Sticky notes should recur when the same idea appears in a new context. Repetition is a feature.

## Understanding questions

Use **understanding questions**, never “interview questions,” in public educational material.

They test whether the reader can reconstruct the reasoning rather than recall a phrase. Keep answers short enough to verify understanding immediately.

Example:

**Why affine?** Because it tests whether the relevant distinction is available through a deliberately small linear readout family before attributing success to nonlinear decoder capacity.

Questions can still incidentally prepare the author or reader for technical discussion; that is not their public purpose.

## Progressive depth

Prefer three levels of explanation:

1. **Main narrative:** intuition and scientific role.
2. **Sticky note:** immediate definition/reminder.
3. **Reference page:** deeper mathematics, assumptions, examples, and links.

A future website should be able to render these levels naturally without rewriting the content.

## Formal checkpoints

Do not copy Lean proof bodies into `research-notes`. Link to the public [`theorem-library`](https://github.com/pH34r-pH/theorem-library), which is authoritative for the public formal source.

When a mathematical result materially supports the narrative, use a compact checkpoint such as:

> **✓ Formal checkpoint — LIB-SPH-002 / FRM-000020**  
> The derivative of nonzero normalization annihilates radial perturbations and scales tangent perturbations by inverse radius.  
> **Established:** local first-order geometry of the normalization map.  
> **Not established:** that radial directions are nuisance or tangent directions are semantic in a trained model.  
> [Explanation →](../reference/formal-methods/checkpoints.md) · [Lean source →](https://github.com/pH34r-pH/theorem-library/blob/main/DomainScaling/Geometry/Sphere/Anisotropy.lean)

Use the stable formal/library identifier where one exists, but do **not** reproduce private theorem-ledger lifecycle state in this repository.

### Epistemic markers

Use these where they improve clarity rather than mechanically decorating every paragraph:

- **✓ Formal checkpoint** — public machine-checkable mathematical statement.
- **● Observation** — measured empirical result under a stated protocol.
- **◇ Assumption** — premise not established by the current evidence.
- **? Hypothesis** — explanation still open to empirical test.

A proof validates its encoded statement and assumptions. Never let the marker silently attach to adjacent empirical interpretation.

## Result boundaries

Every milestone must contain a section titled **What this does not show**.

Separate:

- formal result;
- observation;
- bounded empirical conclusion;
- assumption;
- interpretation;
- speculation;
- active unanswered question.

## Source-of-truth boundary

The repositories deliberately have asymmetric authority:

- `theorem-library`: public Lean source and intrinsic proof/build checks;
- private research laboratory: theorem ledger, ontology/provenance, scientific correspondence, active experimental state;
- `research-notes`: educational narrative and references only.

This repo should never become a second theorem ledger. If a formal result changes, update the explanation/link rather than independently maintaining a competing formal status record here.

## Disclosure boundary

The public repository teaches from stable milestones. It is not a mirror of the private laboratory.

Do not expose unfinished hypotheses, private artifacts, exact active experiment queues, private theorem-ledger research state, or details whose main value is enabling someone to jump directly to the current unpublished frontier.
