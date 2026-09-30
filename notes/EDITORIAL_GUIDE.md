# Editorial Guide

These notes should feel like a good technical textbook that happens to follow a live research program.

## Two layers

### Canonical articles and milestone notebooks

The notebooks preserve the chronological record. Reviewed MyST articles are the reader-facing synthesis and link back to the relevant notebook and references. Both should answer:

1. What question were we trying to answer?
2. Why did the answer matter?
3. What competing explanations were still possible?
4. What experiment separated them?
5. What did we observe?
6. What are we justified in concluding?
7. Which assumptions or limits change its interpretation?
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

State material limits where they affect the interpretation. Canonical articles may use **Interpretation** or a subject-specific heading; preserved notebooks retain their historical structure. Avoid repeating generic disclaimers around every example.

Keep the distinction clear between:

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

## Toy examples and public prose

Label a teaching example once as toy, schematic, or hand-chosen. Explain what it demonstrates and invite a useful edit. Use **Saved output** for its static result and **Your session** for browser output. Repeating that a five-line example is not a model-training replay adds noise.

Keep consequential qualifications specific: the training budget, endpoint versus trajectory, a probe’s readout family, assumptions of a theorem, or the scope of a linked experiment package. State the observation directly before discussing its interpretation.

Consult `pH34r-pH/tone` when editing public prose. Its browser skeleton now contains 370 usable entries; the style guide remains unfrozen. Use baseline-eligible authored text and prefer recent explanatory and technical discussion when editing the current public register. Historical arguments supply evidence about reasoning and syntax, not current beliefs.

The September 2026 article pass used tone revision `96ba26a0b8dbda7a00222a334d429b1aac0cfa8a`, including samples `t1_j20p5ea`, `t1_kg89zsg`, `t1_iikaspv`, and `t1_iioz2oh`. Working choices for this pass were to define the question, expose its premises, develop a concrete comparison, and show how the result changes the next decision. Use first-person explanation where the author describes an actual research choice; use parentheticals for local clarification and keep qualifications attached to the claims they affect. These are provisional editing choices, not a frozen or statistically validated voice profile.

Adapt the explanatory register to a research article. Do not import debate hostility, historical political positions, typos, or borrowed quotations as voice traits. Generated revisions here must not become baseline evidence of the author’s voice.
