# `docs/wiki/` map

These Markdown files are the canonical source copied to the GitHub Wiki by [`../../.github/workflows/wiki-sync.yml`](../../.github/workflows/wiki-sync.yml). Read the repository [`../../AGENTS.md`](../../AGENTS.md) before changing them.

## Page relationships

- `Home.md` and `How-to-Read.md` define the reading path and evidence markers.
- `Research-Chronology.md`, `Current-Frontier.md`, and `Notebook-Guide.md` summarize the public sequence without replacing [`../../CHRONOLOGY.md`](../../CHRONOLOGY.md).
- `Concept-Map.md`, `Evidence-Model.md`, and `Formal-Methods.md` explain reusable structure and claim boundaries.
- `Reproducibility-and-Disclosure.md` carries the public reconstruction and disclosure rules.
- `_Sidebar.md` is the wiki navigation surface.

Keep relative links checkable from the repository and avoid introducing a claim that is not grounded in a repository source. If a page is a summary, link to the authoritative article, notebook, chronology, or reference page rather than copying mutable planning prose.

Validate with:

```sh
git diff --check
python scripts/validate_publication.py
npm run validate:articles
```

The existing wiki-sync workflow publishes these pages; `structural-quality-audit.yml` contains the single changed-Markdown/artifact check. Do not add a second wiki or link-check workflow.
