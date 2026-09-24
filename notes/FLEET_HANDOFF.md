# Fleet handoff: exact Research Notes validation

Research Notes exposes one stable public source gate for Portfolio and Fleet:

- workflow: `.github/workflows/publication-validation.yml`
- job: `publication-integrity`
- contract: `research-notes-publication-validation/v1`
- events: pull requests and pushes to `main`
- authority: public GitHub-hosted runner with `contents: read`

The validator checks the notebook JSON and publication metadata consumed by
Portfolio, local links and referenced local files, and the Markdown reference
tree. It covers `notebooks/*.ipynb` and `reference/**/*.md`; `README.md` and
`CHRONOLOGY.md` are link-checked publication context. The path/content digest is
computed over the covered notebook and reference files. The gate does not run
notebook code, reproduce historical measurements, or review scientific claims.

## Exact-main selection rule

Fleet may select only a full lowercase 40-character Research Notes commit that
is on the observed public `main` history. For that exact SHA, require the newest
`push` run of `publication-validation.yml` with `head_branch == main`, completed
successfully, and a successful job named `publication-integrity`. Missing,
pending, cancelled, failed, PR-only, stale-attempt, or different-SHA evidence
fails closed. A manual Fleet retry must perform the same checks against the
requested exact SHA.

The successful run uploads
`research-notes-validation-<sha>-<run-id>-<attempt>`. Its JSON records the exact
source SHA, run ID and attempt, contract, validated coverage, and
`sha256-path-content-v1` source digest. Fleet's private receipt should preserve
those fields alongside its independently downloaded immutable source-archive
digest. GitHub run and job status establish the gate result; the artifact is
supporting evidence and does not grant deployment authority.

`sha256-path-content-v1` sorts repository-relative POSIX paths, then hashes for
each file: the path byte length as an unsigned eight-byte big-endian integer,
the UTF-8 path bytes, the content byte length in the same integer format, and
the unchanged file bytes. This makes the digest reproducible without running
repository code.

Portfolio may embed the exact Research Notes SHA in a candidate only after this
gate succeeds. Fleet remains responsible for polling public status, verifying
the candidate and exact source identity, and making any protected publication
decision. This repository contains no Azure identity, private credential, Fleet
runner label, or deployment step.
