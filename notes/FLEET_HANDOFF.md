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


## Fleet archive and recovery status

The exact-main check above is now a required input gate for new Portfolio candidate intake. Fleet's [workflow and deployed-surface map](https://github.com/pH34r-pH/long-haul-fleet/blob/main/docs/workflow-and-surface-map.md) describes the six-hour intake poll, Portfolio's exact pinned dependency checks, and the boundary between source qualification, private receipt archival, and protected publication. Research Notes itself has no deployment surface or Azure operation.

The offline verifier merged in Fleet PR [#334](https://github.com/pH34r-pH/long-haul-fleet/pull/334) validates receipt content without credentials. Durable receipt archival and exact-SHA recovery are proposed in draft Fleet PR [#361](https://github.com/pH34r-pH/long-haul-fleet/pull/361), tracked by [Fleet #331](https://github.com/pH34r-pH/long-haul-fleet/issues/331). The authenticated path is not live: Fleet's dedicated App private-key secret is absent, and the App installation still needs Research Notes Actions-read access. [Fleet #363](https://github.com/pH34r-pH/long-haul-fleet/issues/363) tracks those prerequisites and the historical no-Azure validation. Until they pass, treat public artifacts as finite-retention supporting evidence and do not claim durable Fleet recovery has been demonstrated.

