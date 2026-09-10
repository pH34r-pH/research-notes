# Public Formal Checkpoints

This page is an educational index into selected public proofs. It is **not** the theorem ledger and does not own scientific lifecycle status. Follow each link to the public [`theorem-library`](https://github.com/pH34r-pH/theorem-library) for the actual Lean source.

## Hypersphere normalization

### LIB-SPH-002 / FRM-000020 — normalization derivative anisotropy

**Plain-language statement.** For nonzero `x`, the derivative of `x / ||x||` annihilates the radial direction. Perturbations orthogonal to `x` are scaled by `1 / ||x||`; at unit radius they are preserved to first order.

**Why it matters.** Normalization is not locally isotropic. It treats radial and tangent perturbations in mathematically different ways.

**Boundary.** This is a statement about the normalization operation. It does not identify radial directions with nuisance information or tangent directions with semantics in a learned representation.

- [Anisotropy proof](https://github.com/pH34r-pH/theorem-library/blob/main/TheoremLibrary/Geometry/Sphere/Anisotropy.lean)
- [Underlying normalization derivative](https://github.com/pH34r-pH/theorem-library/blob/main/TheoremLibrary/Geometry/Sphere/Normalization.lean)
- [Norm-derivative prerequisite](https://github.com/pH34r-pH/theorem-library/blob/main/TheoremLibrary/Geometry/Sphere/NormDerivative.lean)

### LIB-SPH-003 / FRM-000021 — scale-invariant loss geometry

**Plain-language statement.** Composing a differentiable loss through normalization makes the composed first-order radial sensitivity vanish. For tangent updates, the library also proves exact finite-step norm and derivative-at-zero angular-scaling identities.

**Why it matters.** It separates exact consequences of normalization from stronger optimizer or learning-dynamics claims.

**Boundary.** The theorem does not imply that a particular optimizer follows the idealized update, nor does it establish generalization or task behavior.

- [Scale-invariant loss proof](https://github.com/pH34r-pH/theorem-library/blob/main/TheoremLibrary/Geometry/Sphere/ScaleInvariantLoss.lean)
- [Normalized-loss gradient consequences](https://github.com/pH34r-pH/theorem-library/blob/main/TheoremLibrary/Geometry/Sphere/NormalizationGradient.lean)

### LIB-SPH-001/005 / FRM-000023 — positive-scale quotient and radial-memory boundary

**Plain-language statement.** Positive rescalings of a nonzero proposal produce the same normalized state. Once proposal radius is erased at the normalization boundary, deterministic downstream computation starting from that normalized state cannot recover which positive rescaling was used.

**Why it matters.** It makes precise one kind of information that normalization truly discards.

**Boundary.** An upstream producer can encode previous radial information into angular/tangent structure before normalization. The theorem does not say that all information previously associated with radius must disappear from the complete recurrence.

- [Radial-memory proof](https://github.com/pH34r-pH/theorem-library/blob/main/TheoremLibrary/Geometry/Sphere/RadialMemory.lean)

### FRM-000133 — kernel, range, rank, and singular values

**Plain-language statement.** In finite-dimensional real inner-product spaces, the derivative of normalization has one radial zero mode and equal inverse-radius gain on the tangent modes; the library characterizes its kernel, range, rank, and singular values exactly.

**Why it matters.** The qualitative radial/tangent distinction can be stated as an exact spectral result rather than an informal geometric picture.

- [Normalization spectrum proof](https://github.com/pH34r-pH/theorem-library/blob/main/TheoremLibrary/Geometry/Sphere/NormalizationSpectrum.lean)

### FRM-000149 — composition and gradient boundaries

The public core also contains results about where radial annihilation does and does not survive composition with upstream/downstream maps, plus the actual Riesz gradient of a differentiable normalized loss.

These are useful boundary theorems: they prevent us from taking a true statement about the normalization operator and applying it too broadly to an entire learned recurrence.

- [Normalization composition](https://github.com/pH34r-pH/theorem-library/blob/main/TheoremLibrary/Geometry/Sphere/NormalizationComposition.lean)
- [Normalization gradient](https://github.com/pH34r-pH/theorem-library/blob/main/TheoremLibrary/Geometry/Sphere/NormalizationGradient.lean)

## How to use this index

When a notebook relies on one of these facts, it should give the smallest local explanation needed, mark it as a **✓ Formal checkpoint**, and link here or directly to the Lean source. The notebook should separately identify any empirical assumption needed to connect the theorem to model behavior.

The private theorem ledger remains the authority for scientific correspondence and status; this page is intentionally a readable map, not a synchronized copy of that ledger.
