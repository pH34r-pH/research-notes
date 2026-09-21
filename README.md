# Research Notes

This repository follows an ongoing research project investigating how neural systems represent, transform, preserve, and use information. The work began with experiments treating text as a signal, then gradually expanded into questions about representation geometry, recurrent computation, mathematical constraints on architecture, and the difference between information a model contains and information it actually uses.

The notebooks are arranged in the order those questions developed. They include successful experiments, negative results, corrections to earlier interpretations, mathematical derivations, and experiments I decided not to run after analysis showed they wouldn't answer the intended question. Where later evidence changed my interpretation of an earlier result, I've kept both parts of the story.

The current thread running through the work is a distinction that turned out to matter repeatedly: **what information is preserved in a learned state, what can be recovered from it, what the model itself uses, and what actually affects its behavior.** Those aren't necessarily the same thing.

## Start here

The numbered notebooks follow the research chronologically:

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

The [Visual intuition atlas](notebooks/visual_intuition_atlas.ipynb) is a companion notebook containing small synthetic examples and plots for several of the harder-to-visualize ideas. It is intentionally a work in progress.

## Reading the notes

Technical terms are explained where they first become important, usually with a short **Sticky note** and a link to the deeper [`reference/`](reference/) material. The intended audience is technically experienced, but the notebooks shouldn't require specialized background in geometry, signal processing, formal methods, or representation-learning research just to follow the argument.

I use a few markers when the kind of evidence matters:

- **✓ Formal checkpoint** — a mathematical result established under explicit assumptions, with a public machine-checkable proof where available.
- **● Observation** — something measured under a specified experimental protocol.
- **◇ Assumption** — a premise the current argument depends on without establishing it.
- **? Hypothesis** — an explanation or prediction that remains open to testing.

The distinction matters more than the symbols. A mathematical result doesn't automatically establish its empirical interpretation, and an experimental observation doesn't become a theorem because the explanation is mathematically appealing.

Each milestone also includes **What this does not show**. I use that section to record the strongest interpretation I think the evidence *doesn't* justify, especially when a result is easy to overread.

## References

- [Visual intuition atlas](notebooks/visual_intuition_atlas.ipynb)
- [Concept index](reference/index.md)
- [Glossary](reference/glossary.md)
- [Experimental reasoning](reference/experimental-reasoning.md)
- [Representation and readout](reference/representation-and-readout.md)
- [Formal methods and claim boundaries](reference/formal-methods/index.md)
- [Public formal checkpoints](reference/formal-methods/checkpoints.md)
- [Theorem Library](https://github.com/pH34r-pH/theorem-library)
- [Research chronology](CHRONOLOGY.md)

## Status

Independent research, ongoing.
