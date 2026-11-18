# `articles/` map

Articles are the canonical reader-facing MyST synthesis. Read the repository [`AGENTS.md`](../AGENTS.md), [`notes/EDITORIAL_GUIDE.md`](../notes/EDITORIAL_GUIDE.md), and [`PUBLICATION-DISPOSITIONS.md`](../PUBLICATION-DISPOSITIONS.md) before editing.

## Ownership and relationships

- Numbered `001`–`013` Markdown files are milestone articles with front matter, evidence markers, explicit limits, and links to the source notebook or retained public artifact.
- `accessible-does-not-imply-used.md` is the later companion milestone and has a matching `accessible-vs-used.svg` visual.
- SVGs and other local visuals are article inputs; `references.bib` is the shared citation source.
- `notebooks/` remains the chronological/computational source context. Article prose may synthesize or correct an interpretation, but must not erase the underlying notebook history.

Preserve front-matter fields expected by `scripts/validate_publication.py`, local links, figure/model references, and citation keys. State whether examples are synthetic or exact public reproductions; every mature milestone should retain its “what this does not show” boundary.

## Validation and routing

For article prose, front matter, figures, or citations:

```sh
python scripts/validate_publication.py
python -m unittest discover -s scripts -p 'test_validate_publication.py'
npm run validate:articles
```

If the change alters chronology or an evidence classification, update [`CHRONOLOGY.md`](../CHRONOLOGY.md) or the relevant disposition instead of burying the change in an article-only sentence.
