# Working in Research Notes

Read [`README.md`](README.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), [`CHRONOLOGY.md`](CHRONOLOGY.md), [`PUBLICATION-DISPOSITIONS.md`](PUBLICATION-DISPOSITIONS.md), and [`notes/EDITORIAL_GUIDE.md`](notes/EDITORIAL_GUIDE.md) before changing the public research record.

## Repository map

| Boundary | Responsibility | Read with |
| --- | --- | --- |
| `articles/` | Canonical reader-facing MyST research syntheses and their visual assets. | [`articles/AGENTS.md`](articles/AGENTS.md) |
| `notebooks/` | Chronological computational record and browser-local teaching examples. | [`notebooks/AGENTS.md`](notebooks/AGENTS.md) |
| `reference/` | Reusable concept, method, glossary, and formal-checkpoint material. | [`reference/AGENTS.md`](reference/AGENTS.md) |
| `docs/wiki/` | Canonical source for the GitHub Wiki reading path. | [`docs/wiki/AGENTS.md`](docs/wiki/AGENTS.md) |
| `notes/` | Editorial guidance, publication operations, and future planning; not a replacement for historical evidence. | [`notes/AGENTS.md`](notes/AGENTS.md) |
| `scripts/` | Publication integrity, deterministic coverage, and changed-document/artifact validators. | [`scripts/AGENTS.md`](scripts/AGENTS.md) |
| `.github/workflows/` | Existing publication, structural-audit, and wiki-sync entrypoints. | [`README.md`](README.md) |

## Architecture and data flow

```text
chronology + notebooks + retained public artifacts
        -> reviewed article synthesis + explicit evidence markers
        -> reference/formal-method links and publication dispositions
        -> validate_publication.py + unittest coverage
        -> MyST HTML publication / wiki-sync projection
```

Articles are the primary reader-facing synthesis; notebooks retain chronological and computational context; `reference/` carries reusable explanations and links to the separate Theorem Library; `CHRONOLOGY.md` and `PUBLICATION-DISPOSITIONS.md` define the historical and reader-role mapping. The validators check local links, article figures/cells/citations, notebook dispositions, context pages, and a deterministic source digest.

## Invariants and change routing

- Preserve discovery order, later corrections, negative results, and disclosure dates. A public reconstruction date is not the historical research period.
- Keep formal checkpoints, observations, assumptions, and hypotheses visibly distinct. Never strengthen a claim beyond its cited notebook, artifact, or theorem.
- Treat runnable notebook/article examples as synthetic teaching examples unless an exact public reproduction is explicitly identified.
- Keep private experiment artifacts, active unpublished ledger state, credentials, and deployment material out of this repository.
- When a theorem changes, update the cross-reference to [Theorem Library](https://github.com/pH34r-pH/theorem-library); do not copy proof source here.
- Route reader prose to `articles/`, chronology or computational evidence to `notebooks/` and `CHRONOLOGY.md`, reusable definitions to `reference/`, editorial policy to `notes/`, and publication tooling to `scripts/`.
- Link a superseded plan only to an actual replacement whose identity and relationship are established in the repository; otherwise preserve the open/planning status.

## Focused validation

Run from the repository root:

```sh
git diff --check
python scripts/validate_publication.py
python -m unittest discover -s scripts -p 'test_validate_publication.py'
npm run validate:articles
python scripts/test_docs_hygiene.py
```

Use the validator and unittest for `articles/`, `notebooks/`, `reference/`, `CHRONOLOGY.md`, and dispositions changes; use MyST for rendered article or wiki-facing changes. The existing workflow entrypoints are [`publication-validation.yml`](.github/workflows/publication-validation.yml), [`structural-quality-audit.yml`](.github/workflows/structural-quality-audit.yml), [`documentation-hygiene.yml`](.github/workflows/documentation-hygiene.yml), and [`wiki-sync.yml`](.github/workflows/wiki-sync.yml). Keep `documentation-hygiene.yml` as the single changed-Markdown/artifact guard.

The publication workflow adds `--receipt validation/research-notes-validation.json` with its CI source/run identity; local validation intentionally omits that CI-only receipt metadata.
