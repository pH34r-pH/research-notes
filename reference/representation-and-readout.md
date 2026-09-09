# Representation and Readout

A useful conceptual decomposition is:

`input → representation-producing computation → hidden state → consumer/readout → prediction`

The decomposition is simple, but it prevents several common interpretive mistakes.

## Representation

A representation is an internal state used by a model to carry information forward. Asking whether a representation is “good” is incomplete without specifying *for what downstream operation* and *under what decoder family*.

A representation may preserve a distinction geometrically while a particular consumer ignores it. Conversely, a sufficiently powerful diagnostic may extract a distinction in a way the native architecture could never practically use.

## Readout / consumer

A readout maps a representation to an output. In classification this might be an affine map producing logits followed by softmax. In a language model it ultimately participates in producing a distribution over possible next symbols or tokens.

“Consumer” emphasizes that the downstream mechanism is not merely an observer: it is the part of the actual model that must turn whatever the representation preserved into useful behavior.

## Probe

A probe is a *diagnostic* readout rather than necessarily the model's native one. We choose a probe family to ask a bounded question about recoverability.

For example:

- affine probe → is the distinction linearly accessible (up to bias)?
- shallow nonlinear probe → is it accessible to a modest nonlinear decoder?
- very high-capacity decoder → can provide evidence of recoverability, but makes simplicity and selectivity harder to establish.

Probe families form a ladder rather than a binary “information present / absent” detector.

## Why this decomposition matters

If native predictions are poor, immediately changing the representation mixes two possible bottlenecks: storage/encoding and utilization. Freezing the representation and varying only the readout can localize the problem.

Likewise, finding that a probe succeeds should not tempt us to declare the original model solved: the probe itself may be the missing computation.

## Understanding questions

**Can two consumers behave differently on exactly the same frozen representation?**  
Yes. They may attend to or combine different accessible directions/features.

**If a nonlinear probe succeeds after an affine probe fails, what changed?**  
The representation did not change; the tested decoder family became more expressive.

**Why might the smallest successful consumer be scientifically interesting?**  
It bounds how complicated the missing downstream computation needs to be and helps localize the bottleneck.
