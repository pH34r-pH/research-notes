# Formal Methods in This Research Program

Some parts of this research program are empirical: they depend on trained models, datasets, measurements, and statistical evidence. Other parts are mathematical statements that can be stated precisely enough to prove.

We deliberately keep those two kinds of evidence separate.

## Three repositories, three responsibilities

| Repository | Responsibility | Authoritative for |
|---|---|---|
| [`theorem-library`](https://github.com/pH34r-pH/theorem-library) | Public Lean proofs and proof-checking infrastructure | Public formal source and intrinsic build/check status |
| `domain-scaling-lab` (private) | Active research laboratory, theorem ledger, ontology/provenance, empirical results | Scientific lifecycle and interpretation |
| [`research-notes`](https://github.com/pH34r-pH/research-notes) | Educational narrative | Explanation only; never theorem status |

The separation is intentional. A theorem can be perfectly proved while still being irrelevant to a scientific hypothesis because an assumption does not hold in the trained system. Conversely, an empirical result can be strong without being a theorem.

The Lean namespaces mirror this boundary: reusable public mathematics lives under `TheoremLibrary.*`; research-specific private formalization remains under `DomainScaling.*`. Stable `FRM-*` / `LIB-*` identifiers preserve identity across refactors without making module paths themselves authoritative research IDs.

## The epistemic markers

Research notes use four recurring markers when a distinction is useful:

**✓ Formal checkpoint** — a precise mathematical statement has a public Lean proof at the linked source. This marker refers to the encoded theorem, not to every informal interpretation someone could attach to it.

**● Observation** — something was measured in an experiment under a stated protocol.

**◇ Assumption** — something the argument currently takes as given, either because it is a modeling assumption or because it has not been established by the present experiment.

**? Hypothesis** — a proposed explanation that remains open to empirical discrimination.

These markers are designed to prevent a common reasoning error: silently turning a chain containing observations and assumptions into something that sounds theorem-like.

## Example: normalization geometry

Consider normalization

`N(x) = x / ||x||`, for `x != 0`.

The public Lean library proves an exact local statement about its derivative. The derivative annihilates the radial direction, while tangent perturbations are scaled by the inverse radius. At unit radius, tangent perturbations are fixed to first order.

> **✓ Formal checkpoint — LIB-SPH-002 / FRM-000020**  
> Normalization has an anisotropic derivative: radial gain is zero and tangent gain is `1 / ||x||`.  
> [Lean source →](https://github.com/pH34r-pH/theorem-library/blob/main/TheoremLibrary/Geometry/Sphere/Anisotropy.lean)

That theorem does **not** prove that radial directions represent nuisance information or that tangent directions represent semantics in a trained model.

So an argument might properly be written as:

> ✓ normalization removes infinitesimal radial variation;  
> ● a trained recurrence exhibits a measured directional effect;  
> ◇ the affected directions correspond to a task-relevant/nuisance decomposition;  
> ? normalization may therefore contribute to selective compression.

Only the first item follows from the theorem itself. The other steps require empirical evidence or explicit assumptions.

## Why Lean?

The point is not to formalize every sentence of an ML project. Machine checking is most valuable where a mistaken mathematical intuition could send many experiments in the wrong direction.

Lean helps us make assumptions explicit, distinguish a theorem from its converse, expose missing boundary conditions, and preserve exact statements as the surrounding research changes.

The public [`theorem-library`](https://github.com/pH34r-pH/theorem-library) contains the reusable formal layer and the infrastructure required to independently build and audit it. The private theorem ledger retains richer research metadata such as scientific correspondence, dependencies, review state, and empirical interpretation.

## Stable identifiers

Formal source comments often carry stable identifiers such as `FRM-000020` or library identifiers such as `LIB-SPH-002`. These act as cross-repository addresses.

A research note may use the identifier and link to its proof, but it does not duplicate the private ledger's lifecycle state. If the theorem is refactored, the identifier provides continuity while the source link shows the actual public proof.

## Understanding questions

**Why doesn't a Lean proof automatically validate a scientific claim?**  
Because Lean validates the encoded mathematical statement under its assumptions; correspondence to the real model and empirical validity of those assumptions are separate questions.

**Why keep the theorem ledger private if the proof is public?**  
The ledger contains research-state information: interpretation, dependencies, active questions, and provenance that may expose the current unpublished frontier.

**Why use stable theorem identifiers in public notes?**  
They let different repositories refer to the same formal object without making the educational repo a second source of truth.

**Why separate `TheoremLibrary.*` from `DomainScaling.*`?**  
The namespace itself communicates architectural ownership: reusable public mathematics is upstream, while private research-specific formalization consumes it.

**What does a ✓ Formal checkpoint mean?**  
That the linked mathematical statement has a public machine-checkable proof; it does not grant theorem status to surrounding empirical interpretation.
