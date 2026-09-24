#!/usr/bin/env python3
"""Validate the offline structure consumed by the public notebook publisher.

This gate checks publication inputs and authored local references.  It does not
execute notebook code or assess the scientific conclusions in the notes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

SCHEMA = "research-notes-publication-validation/v1"
SHA = re.compile(r"^[0-9a-f]{40}$")
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
PUBLISHED_ROOTS = ("notebooks", "reference")
CONTEXT_FILES = ("README.md", "CHRONOLOGY.md")


class ValidationError(ValueError):
    """The repository does not satisfy its public publication contract."""


def published_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    for folder in PUBLISHED_ROOTS:
        base = root / folder
        if not base.is_dir():
            raise ValidationError(f"missing publication directory: {folder}")
        paths.extend(path for path in base.rglob("*") if path.is_file())
    if any(path.is_symlink() for folder in PUBLISHED_ROOTS for path in (root / folder).rglob("*")):
        raise ValidationError("publication inputs must not contain symlinks")
    return sorted(paths, key=lambda path: path.relative_to(root).as_posix())


def digest_paths(root: Path, paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        relative = path.relative_to(root).as_posix().encode()
        data = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def markdown_targets(source: str) -> list[str]:
    targets = []
    for match in MARKDOWN_LINK.finditer(source):
        target = match.group(1).strip()
        # Markdown permits an optional quoted title after the destination.
        if target.startswith("<") and ">" in target:
            target = target[1:target.index(">")]
        else:
            target = re.split(r'\s+["\']', target, maxsplit=1)[0]
        targets.append(target)
    return targets


def check_local_links(root: Path, source_path: Path, markdown: str) -> int:
    checked = 0
    for raw in markdown_targets(markdown):
        parsed = urlsplit(raw)
        if parsed.scheme or parsed.netloc or raw.startswith(("#", "mailto:")):
            continue
        destination = unquote(parsed.path)
        if not destination:
            continue
        if destination.startswith("/"):
            raise ValidationError(f"{source_path.relative_to(root)}: repository link must be relative: {raw}")
        target = (source_path.parent / destination).resolve()
        try:
            relative = target.relative_to(root.resolve())
        except ValueError as exc:
            raise ValidationError(f"{source_path.relative_to(root)}: link leaves repository: {raw}") from exc
        if not target.exists():
            raise ValidationError(f"{source_path.relative_to(root)}: missing local target: {relative}")
        checked += 1
    return checked


def load_notebook(path: Path) -> dict:
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"{path.name}: unreadable notebook JSON: {exc}") from exc
    if notebook.get("nbformat") != 4 or not isinstance(notebook.get("cells"), list):
        raise ValidationError(f"{path.name}: expected nbformat 4 with a cells list")
    metadata = notebook.get("metadata")
    if not isinstance(metadata, dict):
        raise ValidationError(f"{path.name}: notebook metadata must be an object")
    publication = metadata.get("publication")
    if not isinstance(publication, dict):
        raise ValidationError(f"{path.name}: missing metadata.publication")
    if publication.get("exampleKind") != "illustrative":
        raise ValidationError(f"{path.name}: exampleKind must be illustrative")
    question = publication.get("question")
    if not isinstance(question, str) or not question.strip():
        raise ValidationError(f"{path.name}: publication question must be non-empty")
    sequence = publication.get("sequence")
    if sequence is not None and (type(sequence) is not int or sequence < 1):
        raise ValidationError(f"{path.name}: sequence must be a positive integer")
    for cell_number, cell in enumerate(notebook["cells"], 1):
        if not isinstance(cell, dict) or cell.get("cell_type") not in {"markdown", "code", "raw"}:
            raise ValidationError(f"{path.name}: malformed cell {cell_number}")
        if not isinstance(cell.get("source", ""), (str, list)):
            raise ValidationError(f"{path.name}: cell {cell_number} source must be text")
        if cell.get("cell_type") == "code" and not isinstance(cell.get("outputs", []), list):
            raise ValidationError(f"{path.name}: code cell {cell_number} outputs must be a list")
    return notebook


def validate(root: Path) -> dict:
    paths = published_files(root)
    allowed = {".ipynb", ".md"}
    unexpected = [path.relative_to(root).as_posix() for path in paths if path.suffix not in allowed]
    if unexpected:
        raise ValidationError(f"unsupported publication input(s): {', '.join(unexpected)}")

    notebooks = sorted(root.joinpath("notebooks").glob("*.ipynb"))
    if not notebooks:
        raise ValidationError("no publishable notebooks found")
    sequences: dict[int, str] = {}
    links_checked = 0
    for path in notebooks:
        notebook = load_notebook(path)
        sequence = notebook["metadata"]["publication"].get("sequence")
        if sequence in sequences:
            raise ValidationError(f"duplicate sequence {sequence}: {sequences[sequence]} and {path.name}")
        if sequence is not None:
            sequences[sequence] = path.name
        for cell in notebook["cells"]:
            if cell["cell_type"] == "markdown":
                source = cell.get("source", "")
                links_checked += check_local_links(root, path, "".join(source) if isinstance(source, list) else source)

    markdown_paths = sorted(root.joinpath("reference").rglob("*.md")) + [root / name for name in CONTEXT_FILES]
    for path in markdown_paths:
        if not path.is_file():
            raise ValidationError(f"missing publication context file: {path.relative_to(root)}")
        links_checked += check_local_links(root, path, path.read_text(encoding="utf-8"))

    return {
        "schema": SCHEMA,
        "coverage": ["notebooks/*.ipynb", "reference/**/*.md"],
        "contextChecked": list(CONTEXT_FILES),
        "sourceDigest": {"algorithm": "sha256-path-content-v1", "value": digest_paths(root, paths)},
        "fileCount": len(paths),
        "notebookCount": len(notebooks),
        "localLinkCount": links_checked,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--source-sha", default=os.environ.get("GITHUB_SHA"))
    parser.add_argument("--run-id", default=os.environ.get("GITHUB_RUN_ID"))
    parser.add_argument("--run-attempt", default=os.environ.get("GITHUB_RUN_ATTEMPT"))
    args = parser.parse_args()
    result = validate(args.root.resolve())
    if args.receipt:
        if not args.source_sha or not SHA.fullmatch(args.source_sha):
            parser.error("--source-sha must be an exact lowercase 40-character commit SHA")
        if (not args.run_id or not args.run_id.isdigit() or int(args.run_id) < 1 or
                not args.run_attempt or not args.run_attempt.isdigit() or int(args.run_attempt) < 1):
            parser.error("--run-id and --run-attempt must be positive integers")
        result.update({"sourceSha": args.source_sha, "runId": int(args.run_id),
                       "runAttempt": int(args.run_attempt)})
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except ValidationError as exc:
        raise SystemExit(f"publication validation failed: {exc}") from exc
