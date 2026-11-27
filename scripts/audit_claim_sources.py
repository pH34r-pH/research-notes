"""Verify claim sources against immutable objects in local Git clones."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

from claim_evidence import load_claims
from validate_publication import markdown_targets


def git_bytes(repository: Path, revision: str, path: str) -> bytes:
    """Read the pinned Git object without trusting the upstream checkout's working files."""
    result = subprocess.run(
        ["git", "-C", str(repository), "show", f"{revision}:{path}"],
        capture_output=True, check=False, env={**os.environ, "GIT_NO_LAZY_FETCH": "1"},
    )
    if result.returncode != 0:
        raise ValueError(f"pinned upstream Git object unavailable at {revision}:{path}")
    return result.stdout


def check_digest(contents: bytes, expected: str, label: str) -> None:
    if hashlib.sha256(contents).hexdigest() != expected:
        raise ValueError(f"upstream {label} digest differs")


def source_path(url: str, revision: str) -> str:
    return urlsplit(url).path.split(f"/blob/{revision}/", 1)[1]


def audit_formal(repository: Path, evidence: dict) -> dict:
    revision = evidence["applicabilityRevision"]
    path = source_path(evidence["applicabilityUrl"], revision)
    applicability = json.loads(git_bytes(repository, revision, path))
    proof = applicability["proof"]
    proof_fields = {
        "declaration": evidence["declaration"], "sourceCommit": evidence["revision"],
        "sourcePath": source_path(evidence["url"], evidence["revision"]), "sourceSha256": evidence["sourceSha256"],
    }
    if applicability["id"] != evidence["formalId"] or any(proof[key] != value for key, value in proof_fields.items()):
        raise ValueError("pinned applicability record names different proof evidence")
    check_digest(git_bytes(repository, evidence["revision"], proof["sourcePath"]),
                 evidence["sourceSha256"], "Lean source")
    return {"declaration": proof["declaration"], "sourceSha256": proof["sourceSha256"],
            "applicabilityRevision": revision}


def audit_experiment(repository: Path, evidence: dict) -> dict:
    revision = evidence["revision"]
    prefix = f"examples/{evidence['finalizationId']}"
    attempt = f"evidence/attempts/{evidence['attemptId']}"
    members = {
        "planSha256": f"{attempt}/plan-package.zip",
        "resultSha256": f"{attempt}/pilot-result.json",
        "attemptSha256": f"evidence/finalization/{evidence['attemptSha256']}/parent-attempt-package.zip",
        "protocolSha256": "experiment/protocol.md",
        "decisionSha256": "evidence/scientific-decision.md",
        "reviewSha256": "evidence/publication-review.md",
        "finalizationSha256": "final.zip",
    }
    for field, path in members.items():
        check_digest(git_bytes(repository, revision, f"{prefix}/{path}"), evidence[field], field)
    evaluator = source_path(evidence["evaluatorUrl"], revision)
    check_digest(git_bytes(repository, revision, evaluator), evidence["evaluatorSha256"], "evaluator")
    recipe = json.loads(git_bytes(repository, revision, f"{prefix}/experiment.json"))
    runner = json.loads(git_bytes(repository, revision, f"{prefix}/{attempt}/runner-receipt.json"))
    walkthrough = git_bytes(repository, revision, source_path(evidence["url"], revision))
    if recipe["id"] != evidence["finalizationId"] or recipe["expectedPackage"]["sha256"] != evidence["finalizationSha256"]:
        raise ValueError("pinned Compiler recipe names a different finalization")
    if runner["attemptId"] != evidence["attemptId"] or runner["planPackageSha256"] != evidence["planSha256"]:
        raise ValueError("pinned runner receipt names a different attempt or plan")
    if f"`{evidence['requestId']}`".encode() not in walkthrough:
        raise ValueError("pinned walkthrough does not identify the requested experiment")
    return {"verifiedFiles": len(members) + 1, "evaluatorSha256": evidence["evaluatorSha256"],
            "finalizationSha256": evidence["finalizationSha256"],
            "attemptId": runner["attemptId"]}


def audit_document(repository: Path, evidence: dict) -> dict:
    revision = evidence["revision"]
    path = source_path(evidence["url"], revision)
    contents = git_bytes(repository, revision, path)
    check_digest(contents, evidence["sourceSha256"], path)
    return {"sourceSha256": evidence["sourceSha256"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compiler", type=Path, required=True)
    parser.add_argument("--theorem-library", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        claims = load_claims(args.root, markdown_targets)
        if not claims:
            raise ValueError("no reviewed claim evidence to audit")
        repositories = {"pH34r-pH/research-notes": args.root, "pH34r-pH/experiment-compiler": args.compiler,
                        "pH34r-pH/theorem-library": args.theorem_library}
        report = {}
        for key, claim in claims.items():
            evidence = claim["evidence"]
            if evidence["kind"] == "lean":
                report[key] = audit_formal(args.theorem_library, evidence)
            elif evidence["kind"] == "compiled-experiment":
                report[key] = audit_experiment(args.compiler, evidence)
            else:
                report[key] = audit_document(repositories[evidence["repository"]], evidence)
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        parser.exit(1, f"claim source audit failed: {exc}\n")
    print(json.dumps({"sourceAudit": "verified", "claims": report}, sort_keys=True))


if __name__ == "__main__":
    main()
