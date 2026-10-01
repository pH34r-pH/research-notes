# `reference/` map

`reference/` is the reusable methods and concepts layer between the reader-facing articles and the chronological notebooks. Read the repository [`AGENTS.md`](../AGENTS.md) and [`notes/EDITORIAL_GUIDE.md`](../notes/EDITORIAL_GUIDE.md) first.

## Ownership

- `index.md` is the concept entrypoint; `glossary.md` defines recurring terms.
- `experimental-reasoning.md` and `representation-and-readout.md` explain reusable reasoning distinctions.
- `formal-methods/` contains the formal-methods entrypoint, checkpoints, and links to promoted Theorem Library results.

Reference pages may clarify a concept used by multiple articles, but they must preserve claim strength and point back to the source article/notebook where evidence lives. Formal links identify mathematical results under explicit assumptions; they do not convert empirical observations into theorems.

## Change routing and validation

Route a new public theorem link through [`formal-methods/checkpoints.md`](formal-methods/checkpoints.md) and the corresponding Theorem Library source. Route a new term through `glossary.md`; route a milestone-specific argument to `articles/`.

```sh
python scripts/validate_publication.py
python -m unittest discover -s scripts -p 'test_validate_publication.py'
```
