# Formal methods

Formal methods are used when mathematics can remove ambiguity before another training run.

## Why formalize

A proof or counterexample can:

- establish a property an experiment would otherwise rediscover;
- show a proposed mechanism is impossible as stated;
- expose an assumption that requires empirical validation;
- distinguish a local operator fact from a stronger recurrent-system claim;
- eliminate an experiment that cannot discriminate its intended hypotheses.

## Example: normalization

For nonzero `x`, the derivative of `x / ||x||` has an exact radial/tangent structure. That result establishes how the normalization operator treats infinitesimal perturbations.

It does **not** establish that radial information is useless, tangent variation is semantic, or normalization improves a trained model.

## Public proof boundary

Research Notes explains the research use and non-claim. [Theorem Library](https://github.com/pH34r-pH/theorem-library) contains the Lean proof. The public [formal checkpoint index](https://github.com/pH34r-pH/research-notes/blob/main/reference/formal-methods/checkpoints.md) maps stable identifiers to the notes that use them.

The formal layer is a tool for claim discipline, not an attempt to formalize the entire empirical program.
