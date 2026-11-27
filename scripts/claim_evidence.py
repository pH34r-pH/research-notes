"""Validate public claim bindings and report editorial impact offline."""
from __future__ import annotations

import json
import posixpath
import re
from collections.abc import Callable
from pathlib import Path

RECORD = "reference/claim-evidence.json"
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
ARTICLE_PATH = re.compile(r"(?:articles|reference)/(?:[A-Za-z0-9_-]+/)*[A-Za-z0-9_-]+\.md")
COMMIT = re.compile(r"[0-9a-f]{40}")
DIGEST = re.compile(r"[0-9a-f]{64}")
PINNED_GITHUB = re.compile(r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/blob/([0-9a-f]{40})/.+")
PACKAGE_DIGESTS = ("planSha256", "attemptSha256", "resultSha256", "protocolSha256",
                   "decisionSha256", "reviewSha256", "finalizationSha256", "evaluatorSha256")
DOCUMENT_STATUSES = {
    "assumption": {"design-premise", "historical-premise"},
    "conclusion": {"documented"},
    "correction": {"empirical-evidence-unverified"},
    "counterexample": {"illustrative"},
    "formal": {"documented"},
    "hypothesis": {"open"},
    "limitation": {"documented"},
    "observation": {"empirical-evidence-unverified"},
}


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for name, value in pairs:
        if name in result:
            raise ValueError(f"duplicate claim evidence key {name}")
        result[name] = value
    return result


def _matches(pattern: re.Pattern, value: object) -> bool:
    return isinstance(value, str) and pattern.fullmatch(value) is not None


def _section(root: Path, passage: object) -> tuple[str, str]:
    if not isinstance(passage, dict) or set(passage) != {"path", "anchor"}:
        raise ValueError("a claim needs a passage path and anchor")
    path, anchor = passage["path"], passage["anchor"]
    if not _matches(ARTICLE_PATH, path) or not _matches(SLUG, anchor):
        raise ValueError("invalid claim passage path or anchor")
    page = root / path
    if not page.is_file():
        raise ValueError(f"claim passage is missing at {path}")
    source = page.read_text(encoding="utf-8")
    markers = list(re.finditer(rf"^\({re.escape(anchor)}\)=\s*\n(#+)\s+[^\n]+", source, re.MULTILINE))
    if len(markers) != 1:
        raise ValueError(f"claim anchor {anchor} must precede exactly one heading in {path}")
    start = markers[0].end()
    depth = len(markers[0][1])
    boundary = re.search(rf"^#{{1,{depth}}}\s", source[start:], re.MULTILINE)
    end = start + boundary.start() if boundary else len(source)
    return path, source[start:end]


def _pinned(value: object, repository: object, revision: object) -> bool:
    match = PINNED_GITHUB.fullmatch(value) if isinstance(value, str) else None
    return match is not None and match.groups() == (repository, revision)


def _formal_links(claim: dict, evidence: dict) -> set[str]:
    formal_id = evidence.get("formalId")
    if (
        claim["kind"] != "formal" or evidence["repository"] != "pH34r-pH/theorem-library"
        or not isinstance(evidence.get("declaration"), str)
        or not _matches(DIGEST, evidence.get("sourceSha256"))
        or not _matches(re.compile(r"FRM-[0-9]{6}"), formal_id)
    ):
        raise ValueError("formal claim needs a Lean declaration and source digest")
    applicability = evidence.get("applicabilityUrl")
    if not _pinned(applicability, evidence["repository"], evidence.get("applicabilityRevision")):
        raise ValueError("theorem applicability link must use an exact public revision")
    if formal_id == "FRM-000133" or claim["id"] == "normalization-spectrum-local-derivative":
        if "nonzero-input" not in claim["assumptions"]:
            raise ValueError("FRM-000133 requires the nonzero-input premise")
        if (
            formal_id != "FRM-000133"
            or evidence["declaration"] != "TheoremLibrary.Geometry.Sphere.normalization_singularValues"
            or claim.get("scope") != "one-local-derivative"
            or claim.get("runtimeApplicability") != "unmeasured"
        ):
            raise ValueError("FRM-000133 requires its local derivative and unmeasured runtime scope")
    return {applicability}


def _experiment_links(claim: dict, evidence: dict) -> set[str]:
    if (
        claim["kind"] != "observation"
        or evidence["repository"] != "pH34r-pH/experiment-compiler"
        or not all(_matches(DIGEST, evidence.get(field)) for field in PACKAGE_DIGESTS)
    ):
        raise ValueError("empirical claim requires exact Compiler evidence digests")
    for field in ("requestId", "attemptId", "finalizationId", "comparison"):
        if not _matches(SLUG, evidence.get(field)):
            raise ValueError(f"empirical claim is missing a stable {field}")
    reader_url = f"https://experiments.tyharbin.com/experiments/{evidence['finalizationId']}/"
    if evidence.get("readerUrl") != reader_url:
        raise ValueError("empirical reader link disagrees with the finalization ID")
    if not isinstance(claim.get("observations"), dict) or not claim["observations"]:
        raise ValueError("empirical claim needs a source observation record")
    evaluator_url = evidence.get("evaluatorUrl")
    if not _pinned(evaluator_url, evidence["repository"], evidence["revision"]) or evaluator_url == evidence["url"]:
        raise ValueError("empirical claim requires an evaluator pinned to the exact Compiler revision")
    return {reader_url, evaluator_url}


def _document_links(claim: dict, evidence: dict) -> set[str]:
    if claim["status"] not in DOCUMENT_STATUSES.get(claim["kind"], set()):
        raise ValueError(f"{claim['id']} has an invalid status for a documented claim")
    if not isinstance(claim.get("statement"), str) or not claim["statement"].strip():
        raise ValueError(f"{claim['id']} needs a statement that identifies the claim")
    if not _matches(DIGEST, evidence.get("sourceSha256")):
        raise ValueError(f"{claim['id']} requires a pinned source document digest")
    if claim["kind"] == "correction" and not claim.get("supersedes"):
        raise ValueError(f"{claim['id']} must identify the earlier claim it corrects")
    return set()


def _validate_claim(root: Path, claim: dict, markdown_targets: Callable[[str], list[str]]) -> None:
    path, section = _section(root, claim.get("passage"))
    evidence = claim.get("evidence")
    if not isinstance(evidence, dict) or not _pinned(
        evidence.get("url"), evidence.get("repository"), evidence.get("revision"),
    ):
        raise ValueError(f"{claim['id']} requires an evidence URL pinned to its exact revision")
    for field in ("assumptions", "limitations"):
        items = claim.get(field)
        if not isinstance(items, list) or not items or not all(_matches(SLUG, item) for item in items):
            raise ValueError(f"{claim['id']} requires explicit {field}")
    if not _matches(SLUG, claim.get("status")):
        raise ValueError(f"{claim['id']} requires an evidence status")
    if not _matches(SLUG, claim.get("kind")):
        raise ValueError(f"{claim['id']} has an unknown evidence kind")
    validators = {"lean": _formal_links, "compiled-experiment": _experiment_links, "source-document": _document_links}
    evidence_kind = evidence.get("kind")
    if not isinstance(evidence_kind, str) or evidence_kind not in validators:
        raise ValueError(f"{claim['id']} has an unknown evidence kind")
    expected = validators[evidence_kind](claim, evidence) | {
        evidence["url"], posixpath.relpath(RECORD, posixpath.dirname(path)),
    }
    if not expected.issubset(markdown_targets(section)):
        raise ValueError(f"{claim['id']} passage must link to its claim record and exact evidence")


def _check_supersession(claims: dict[str, dict]) -> None:
    for claim_id in claims:
        cursor = claim_id
        visited: set[str] = set()
        while cursor is not None:
            if cursor in visited:
                raise ValueError(f"claim supersession has a cycle at {cursor}")
            visited.add(cursor)
            supersedes = claims[cursor].get("supersedes")
            if not isinstance(supersedes, list) or len(supersedes) > 1:
                raise ValueError(f"{cursor} supersedes at most one immediate claim")
            cursor = supersedes[0] if supersedes else None
            if supersedes and (not isinstance(cursor, str) or cursor not in claims):
                raise ValueError(f"unknown superseded claim in the chain for {claim_id}")


def load_claims(root: Path, markdown_targets: Callable[[str], list[str]]) -> dict[str, dict]:
    path = root / RECORD
    if not path.is_file():
        return {}
    document = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    if not isinstance(document, dict) or document.get("schema") != "research-notes-claim-evidence/v1":
        raise ValueError("unsupported claim evidence schema")
    rows = document.get("claims")
    if not isinstance(rows, list) or not rows:
        raise ValueError("claim evidence record must name at least one claim")
    claims: dict[str, dict] = {}
    for claim in rows:
        if not isinstance(claim, dict) or not _matches(SLUG, claim.get("id")) or claim["id"] in claims:
            raise ValueError("invalid or duplicate claim ID")
        _validate_claim(root, claim, markdown_targets)
        claims[claim["id"]] = claim
    _check_supersession(claims)
    return claims


def review_impact(claims: dict[str, dict], evidence_id: str, proposed: str) -> list[dict]:
    if not (_matches(COMMIT, proposed) or _matches(DIGEST, proposed)):
        raise ValueError("proposed evidence identity must be an exact commit or SHA-256 digest")
    affected = []
    for claim_id, claim in claims.items():
        evidence = claim["evidence"]
        evaluator_url = evidence.get("evaluatorUrl")
        if evidence_id not in (evidence.get("formalId"), evidence.get("finalizationId"), evidence["url"],
                               evaluator_url):
            continue
        current = evidence["revision"]
        if len(proposed) == 64:
            current = (evidence["evaluatorSha256"] if evidence_id == evaluator_url
                       else evidence.get("finalizationSha256", evidence.get("sourceSha256")))
        if current != proposed:
            affected.append({"claimId": claim_id, "passage": claim["passage"], "retainedIdentity": current,
                             "reason": "upstream evidence identity changed"})
    return affected
