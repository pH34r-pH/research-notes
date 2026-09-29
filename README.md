# Research Notes

[![Publication validation](https://github.com/pH34r-pH/research-notes/actions/workflows/publication-validation.yml/badge.svg)](https://github.com/pH34r-pH/research-notes/actions/workflows/publication-validation.yml)
[![License](https://img.shields.io/github/license/pH34r-pH/research-notes)](LICENSE)

<p align="center">
  <img src="docs/assets/hero.webp" alt="Research Notes — cyberpunk orbital research workspace and connected knowledge surfaces" width="100%">
</p>

**An evolving research record on representation, geometry, information, and computation in neural systems.**

This repository follows the questions in the order they developed. It includes positive results, negative results, mathematical derivations, later corrections, and experiments that were abandoned after analysis showed they would not answer the intended question.

The current thread running through the work is a distinction that repeatedly matters:

> **Information preserved in a learned state, information recoverable from it, information the model itself uses, and information that causally affects behavior are not necessarily the same thing.**

## Start with the notebooks

1. [What if text were a signal?](notebooks/001_text_as_signal.ipynb)
2. [Where did the spectral loss occur?](notebooks/002_locating_representation_loss.ipynb)
3. [Coordinates matter; operations matter more](notebooks/003_coordinates_and_matched_operations.ipynb)
4. [Isolating the phase-aware mechanism](notebooks/004_isolating_phase_attention.ipynb)
5. [The unit-hypersphere anomaly](notebooks/005_unit_hypersphere_anomaly.ipynb)
6. [A dramatic endpoint can still mislead](notebooks/006_endpoint_can_mislead.ipynb)
7. [Derive before training](notebooks/007_derive_before_training.ipynb)
8. [What does the sphere actually do?](notebooks/008_frozen_mechanism_tests.ipynb)
9. [From hypothesis sprawl to a theorem ledger](notebooks/009_theorem_ledger_method.ipynb)
10. [What state should a reasoner preserve?](notebooks/010_dynamic_quotient.ipynb)
11. [Geometry should follow invariance, not aesthetics](notebooks/011_geometry_from_invariance.ipynb)
12. [Natural-source task distinctions](notebooks/012_natural_source_distinctions.ipynb)
13. [Accessible does not imply used](notebooks/013_accessible_not_used.ipynb)

The [Visual Intuition Atlas](notebooks/visual_intuition_atlas.ipynb) is a companion set of synthetic examples for difficult geometric ideas.

For the larger map, use the [Wiki](https://github.com/pH34r-pH/research-notes/wiki), [research chronology](CHRONOLOGY.md), and [concept index](reference/index.md).

## How claims are marked

- **✓ Formal checkpoint** — established mathematically under explicit assumptions.
- **● Observation** — measured under a specified protocol.
- **◇ Assumption** — used by the argument but not established there.
- **? Hypothesis** — still open to testing.

The distinction matters more than the symbols. A theorem does not automatically establish its empirical interpretation, and an observation does not become a theorem because its explanation is mathematically attractive.

Each mature milestone also records **What this does not show**.

## Research architecture

```text
private experiments / active reasoning
            |
      stable result
            |
 interpretation review
            |
 public theorem promotion (when applicable)
            |
            v
      numbered notebook
            |
            +--> reusable reference pages
            +--> Theorem Library proof links
            +--> public reproducibility artifacts
```

The notebooks are the narrative layer. `reference/` is the reusable explanatory layer. [Theorem Library](https://github.com/pH34r-pH/theorem-library) is the public machine-checkable mathematics layer.

## Reproducibility and disclosure

Runnable notebook code is a synthetic teaching example unless explicitly identified as an exact replay/public artifact. Research period and public reconstruction date are kept separate. Later corrections remain visible rather than rewriting the earlier result.

The [chronology manifest](CHRONOLOGY.md) documents the reconstruction and disclosure rules.

## Contributing and citation

Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing editorial or technical changes. Research references should identify the specific notebook/artifact and may use [CITATION.cff](CITATION.cff) for repository-level metadata.

Licensed under Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
