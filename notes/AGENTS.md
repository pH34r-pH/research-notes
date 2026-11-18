# `notes/` map

`notes/` contains editorial and operational guidance, not a replacement for the public chronology or source evidence. Read the repository [`AGENTS.md`](../AGENTS.md) and [`notes/EDITORIAL_GUIDE.md`](EDITORIAL_GUIDE.md) first.

- `EDITORIAL_GUIDE.md` defines the two-layer reading model, epistemic markers, result boundaries, and disclosure boundary.
- `FLEET_HANDOFF.md` records the exact-main validation handoff and archive/recovery context; preserve its operational distinctions.
- `FUTURE_MILESTONES.md` is planning state and must not be presented as completed evidence.
- `PUBLICATION.md` describes the policy for public teaching examples.

Route historical evidence to [`CHRONOLOGY.md`](../CHRONOLOGY.md), reader synthesis to [`articles/`](../articles/), and reusable methods to [`reference/`](../reference/). Update plans only when their replacement or status is evidenced; do not mark a plan superseded merely because a newer idea exists.

For changes that affect published inputs or disclosure rules, run:

```sh
python scripts/validate_publication.py
python -m unittest discover -s scripts -p 'test_validate_publication.py'
```
