# Reproducibility and disclosure

The public repository is a curated research record, not a dump of every private run.

## Public notebooks

Runnable code in a notebook is a synthetic teaching example unless the text explicitly identifies it as an exact replay or public artifact. This prevents explanatory code from inheriting the provenance of a private experiment.

## Historical reconstruction

Public reconstructions preserve discovery order and later corrections. They do not rewrite Git history to create a false publication timeline.

## Private-to-public boundary

Private experiment artifacts, active queues, unpublished hypotheses, and theorem-ledger lifecycle state remain private until a stable result and disclosure decision exist.

The general publication path is:

```text
active question
 -> stable result
 -> interpretation review
 -> public theorem promotion where applicable
 -> notebook / canonical MyST article source
 -> Portfolio exposition
 -> exact Experiment Compiler reproduction identity
 -> optional reviewed compiled-experiments archival release
 -> owner-controlled Zenodo DOI
```

## Standards and compiled experiments

Where a study reaches a reproducibility boundary, the broader project can use the public Experiment Compiler to build an explicit shareable closure. Research Notes should link to that artifact rather than embedding a second hand-maintained copy of its metadata.

See [CHRONOLOGY.md](https://github.com/pH34r-pH/research-notes/blob/main/CHRONOLOGY.md) for disclosure rules.


## Archival releases

The live reproduction object and the scholarly archive are distinct.

- Experiment Compiler / `experiments.tyharbin.com` owns the exact package identity, lifecycle, and inspect/verify/run presentation.
- `pH34r-pH/compiled-experiments` may preserve the exact source-owner-approved finalized public bytes in an immutable reviewed GitHub Release.
- Zenodo may archive that reviewed release and mint a DOI only through the explicit owner publication step.
- Research Notes may record the exact release/DOI as citation metadata after it exists; it does not mirror the package or maintain another status registry.

A DOI does not establish scientific acceptance or independent reproduction. See `pH34r-pH/compiled-experiments#1`.
