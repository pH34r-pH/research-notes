# `scripts/` map

The scripts implement the publication contract described by the repository [`AGENTS.md`](../AGENTS.md). Keep them deterministic and fail closed.

- `validate_publication.py` checks local Markdown links, article metadata/figures/cells/citations, notebook dispositions, context pages, and writes the source-digest receipt.
- `test_validate_publication.py` is the executable contract for those checks, including missing-link, visualization, metadata, disposition, and digest failures.
- `docs_hygiene.py` / `test_docs_hygiene.py` check changed living-document names, actual Git rename destinations, and incidental artifacts; the workflow sends changed living Markdown to pinned style/link tools.

Keep `documentation-hygiene.yml` as the single changed-Markdown/artifact guard; do not add another framework.

```sh
python scripts/validate_publication.py
python -m unittest discover -s scripts -p 'test_validate_publication.py'
python scripts/test_docs_hygiene.py
npm run validate:articles
```
