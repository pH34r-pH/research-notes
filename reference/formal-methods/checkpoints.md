# Public formal checkpoints

This page connects mathematical results used in the research notes to their public Lean proofs. Each checkpoint states the result in ordinary language, explains why it matters to the research, and keeps the scientific interpretation separate from what the theorem itself establishes.

## LIB-SPH-002 / FRM-000020 — normalization derivative anisotropy

**Statement.** For nonzero `x`, the derivative of `x / ||x||` annihilates the radial direction. Perturbations orthogonal to `x` are scaled by `1 / ||x||`; at unit radius they are preserved to first order.

**Research use.** This gives an exact version of the radial/tangent distinction that motivated later mechanism tests. Normalization is locally anisotropic rather than treating every perturbation direction equally.

**Boundary.** The theorem does not identify radial variation with nuisance information or tangent variation with semantics in a learned representation.

**Used in:** [007 — Derive before training](../../notebooks/007_derive_before_training.ipynb), [008 — What does the sphere actually do?](../../notebooks/008_frozen_mechanism_tests.ipynb)

**Proof:** [Anisotropy.lean](https://github.com/pH34r-pH/theorem-library/blob/main/TheoremLibrary/Geometry/Sphere/Anisotropy.lean) · [Normalization.lean](https://github.com/pH34r-pH/theorem-library/blob/main/TheoremLibrary/Geometry/Sphere/Normalization.lean) · [NormDerivative.lean](https://github.com/pH34r-pH/theorem-library/blob/main/TheoremLibrary/Geometry/Sphere/NormDerivative.lean)

## LIB-SPH-003 / FRM-000021 — scale-invariant loss geometry

**Statement.** Composing a differentiable loss through normalization removes first-order radial sensitivity. The library also proves exact identities for normalized tangent updates and their angular scaling.

**Research use.** These results separate consequences that follow directly from normalization from stronger claims about optimization or learning dynamics.

**Boundary.** They do not imply that a particular optimizer follows an idealized update, or that normalization improves generalization or task performance.

**Used in:** [007 — Derive before training](../../notebooks/007_derive_before_training.ipynb), with later mechanism context in [008](../../notebooks/008_frozen_mechanism_tests.ipynb)

**Proof:** [ScaleInvariantLoss.lean](https://github.com/pH34r-pH/theorem-library/blob/main/TheoremLibrary/Geometry/Sphere/ScaleInvariantLoss.lean) · [NormalizationGradient.lean](https://github.com/pH34r-pH/theorem-library/blob/main/TheoremLibrary/Geometry/Sphere/NormalizationGradient.lean)

## LIB-SPH-001/005 / FRM-000023 — positive-scale quotient and radial-memory boundary

**Statement.** Positive rescalings of a nonzero proposal produce the same normalized state. Once proposal radius has been erased at that boundary, deterministic downstream computation starting only from the normalized state cannot determine which positive rescaling produced it.

**Research use.** This identifies one specific kind of information that normalization genuinely discards and gives a precise boundary for radial-memory explanations.

**Boundary.** Upstream computation can encode information previously associated with radius into direction before normalization. The result therefore does not say that every piece of information ever carried by magnitude disappears from the complete recurrence.

**Used in:** [008 — What does the sphere actually do?](../../notebooks/008_frozen_mechanism_tests.ipynb)

**Proof:** [RadialMemory.lean](https://github.com/pH34r-pH/theorem-library/blob/main/TheoremLibrary/Geometry/Sphere/RadialMemory.lean)

## FRM-000133 — normalization spectrum

**Statement.** In finite-dimensional real inner-product spaces, the derivative of normalization has one radial zero mode and equal inverse-radius gain on tangent modes. Its kernel, range, rank, and singular values can therefore be characterized exactly.

**Research use.** This turns the qualitative radial/tangent picture into an exact spectral statement and clarifies what one-step normalization can and cannot selectively contract.

**Boundary.** A spectrum for one local derivative does not determine the spectrum or behavior of a finite-horizon recurrent Jacobian product.

**Used in:** [007](../../notebooks/007_derive_before_training.ipynb) and [008](../../notebooks/008_frozen_mechanism_tests.ipynb)

**Proof:** [NormalizationSpectrum.lean](https://github.com/pH34r-pH/theorem-library/blob/main/TheoremLibrary/Geometry/Sphere/NormalizationSpectrum.lean)

## FRM-000149 — composition and gradient boundaries

**Statement.** The public library records conditions under which radial annihilation survives or fails to survive composition with surrounding maps, together with exact gradient identities for differentiable losses composed with normalization.

**Research use.** These are boundary results: they prevent a true statement about the normalization operator from being applied automatically to an entire learned recurrence.

**Boundary.** The surrounding network can mix directions before or after normalization, so local radial annihilation does not imply global radial irrelevance.

**Used in:** [008 — What does the sphere actually do?](../../notebooks/008_frozen_mechanism_tests.ipynb)

**Proof:** [NormalizationComposition.lean](https://github.com/pH34r-pH/theorem-library/blob/main/TheoremLibrary/Geometry/Sphere/NormalizationComposition.lean) · [NormalizationGradient.lean](https://github.com/pH34r-pH/theorem-library/blob/main/TheoremLibrary/Geometry/Sphere/NormalizationGradient.lean)

## Following a checkpoint

The notebook gives the local explanation needed to follow the research. This index records the statement, research use, and boundary in one place. The linked Lean source is the machine-checkable mathematical version for readers who want to inspect the exact assumptions or proof.

Additional stable formal results can be added here as they become part of the public research narrative.
