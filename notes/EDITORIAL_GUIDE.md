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

## Result boundaries

Every milestone must contain a section titled **What this does not show**.

Separate:

- observation;
- bounded empirical conclusion;
- interpretation;
- speculation;
- active unanswered question.

## Disclosure boundary

The public repository teaches from stable milestones. It is not a mirror of the private laboratory.

Do not expose unfinished hypotheses, private artifacts, exact active experiment queues, or details whose main value is enabling someone to jump directly to the current unpublished frontier.
