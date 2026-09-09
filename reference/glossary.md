# Glossary

Short definitions are intentionally written for recall and use. Milestone notebooks may contain even shorter sticky-note versions; this page is the canonical place to expand them.

## Affine map

An affine map has the form

`z = Wx + b`

where `W` is a linear transformation and `b` is a bias or translation. Compared with a purely linear map, the bias allows the output to shift away from the origin. An affine map can mix, rotate, rescale, project, and shift coordinates, but it cannot create genuinely nonlinear feature interactions by itself.

**In this project:** an affine probe is deliberately small. If it recovers a distinction from a frozen state, that distinction is accessible without requiring a deep nonlinear decoder.

**Understanding question:** Why is affine-probe success a stronger simplicity claim than success with a large multilayer network?

## Logit

A logit is an unnormalized score produced before converting scores into probabilities. In a classifier, larger logits generally correspond to greater predicted preference for a class, but logits themselves do not need to sum to one or lie between zero and one.

**Understanding question:** Why can adding the same constant to every class logit leave softmax probabilities unchanged?

## Softmax

Softmax converts a vector of logits into positive probabilities that sum to one:

`softmax(z)_i = exp(z_i) / sum_j exp(z_j)`

It changes how scores are represented as probabilities, but when its input logits are affine functions of the representation, pairwise class decision boundaries remain affine.

**Understanding question:** Why doesn't adding softmax to an affine classifier give it arbitrary nonlinear decision boundaries in the input representation?

## Probe

A probe is a diagnostic model trained on a representation to test whether some target information can be recovered from it by a specified model family. Probe conclusions are always relative to that family and the experimental protocol.

A successful probe establishes accessibility to the probe family; it does not by itself establish that the original model causally uses the information.

**Understanding question:** What additional experiment would you want before replacing “accessible” with “used”?

## Frozen representation

A representation is frozen when the model producing it is held fixed while a downstream diagnostic or consumer is trained or evaluated. This isolates downstream recoverability from representation learning.

**Understanding question:** If the representation were allowed to train with the probe, what alternative explanation would become possible?

## Held-out evaluation

Held-out evaluation measures performance on examples that were not used to fit the evaluated model or tune decisions that would leak information about those examples. The exact independence boundary matters: examples can be nominally separate yet still share dependent sources or lineages.

**Understanding question:** Why might splitting individual observations randomly be insufficient when many observations come from the same source lineage?

## Selectivity

Selectivity is the idea that a diagnostic should succeed on the intended structure while appropriately failing controls where that structure has been destroyed or replaced. It helps distinguish meaningful recoverability from a probe pipeline that can manufacture performance from artifacts.

**Understanding question:** What would it mean if a probe performed almost as well after labels were randomly shuffled?

## Control

A control is a comparison designed to isolate an explanation. Positive controls test whether the machinery can detect an effect that should exist; negative controls test whether it spuriously reports an effect when the relevant relationship has been removed.

**Understanding question:** Why are both positive and negative controls useful when interpreting a failed experiment?

## Ablation

An ablation deliberately removes, replaces, or disables a component to test how the system changes without it. Good ablations are matched closely enough that the removed component, rather than an unrelated perturbation, explains the difference.

**Understanding question:** Why can an unmatched ablation produce an apparently causal result for the wrong reason?

## Causal intervention

A causal intervention changes a candidate mechanism while holding relevant alternatives controlled, then measures the resulting behavior. This is stronger than merely observing that a variable correlates with an outcome.

**Understanding question:** Why is decoding information from a hidden state observational evidence rather than automatically a causal intervention?
