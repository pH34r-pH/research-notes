# `notebooks/` map

Notebooks are the chronological computational record. Read the repository [`AGENTS.md`](../AGENTS.md), [`CHRONOLOGY.md`](../CHRONOLOGY.md), and [`PUBLICATION-DISPOSITIONS.md`](../PUBLICATION-DISPOSITIONS.md) before editing.

## Data flow and invariants

The numbered notebooks provide source context for the numbered articles; publication dispositions identify which notebook sequence, article, and reader role correspond. The Visual Intuition Atlas is a companion collection of synthetic geometric examples. Notebook code is not an exact scientific replay unless the repository explicitly names a retained public artifact and scope.

Preserve chronological order, original computational history, disclosure/reconstruction distinctions, and explicit caveats. Do not replace an earlier notebook result with a later interpretation; record the later correction in the appropriate article, chronology, or disposition document.

## Change routing and validation

- Notebook content or metadata: update the matching disposition/article relationship when needed.
- Reusable definitions or formal links: route them to [`reference/`](../reference/) and the Theorem Library cross-reference rather than duplicating proof source.
- Public artifact identity or exact replay claim: route to the owning evidence/disclosure documentation and verify the exact source.

```sh
python scripts/validate_publication.py
python -m unittest discover -s scripts -p 'test_validate_publication.py'
```
