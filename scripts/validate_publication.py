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

SCHEMA = "research-notes-publication-validation/v2"
SHA = re.compile(r"^[0-9a-f]{40}$")
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FIGURE_DIRECTIVE = re.compile(r"^\s*```\{figure\}\s+(\S+)", re.MULTILINE)
CODE_CELL = re.compile(r"^\s*```\{code-cell\}\s+([\w+-]+)(.*?)^```\s*$", re.MULTILINE | re.DOTALL)
PUBLISHED_ROOTS = ("notebooks", "reference", "articles")
BUILD_INPUTS = ("myst.yml", "package.json", "package-lock.json")
CONTEXT_FILES = ("README.md", "CHRONOLOGY.md", "PUBLICATION-DISPOSITIONS.md", "index.md")


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


def _validate_article_figures(root: Path, path: Path, relative: str, body: str) -> int:
    figure_targets = FIGURE_DIRECTIVE.findall(body)
    if not figure_targets:
        raise ValidationError(f"{relative}: article needs at least one static MyST figure")
    for raw in figure_targets:
        parsed = urlsplit(raw)
        if parsed.scheme or parsed.netloc or raw.startswith("#"):
            raise ValidationError(f"{relative}: figure must use a repository-local asset: {raw}")
        target = (path.parent / unquote(parsed.path)).resolve()
        try:
            target.relative_to(root.resolve())
        except ValueError as exc:
            raise ValidationError(f"{relative}: figure asset leaves repository: {raw}") from exc
        if not target.is_file():
            raise ValidationError(f"{relative}: missing figure asset: {raw}")
        if target.suffix.lower() not in {".svg", ".png", ".jpg", ".jpeg", ".webp"}:
            raise ValidationError(f"{relative}: unsupported figure asset type: {raw}")
    return len(figure_targets)


def _validate_article_cells(relative: str, body: str) -> int:
    cells = list(CODE_CELL.finditer(body))
    for cell in cells:
        info = cell.group(2)
        tags = re.search(r"^:tags:\s*\[(.*?)\]\s*$", info, re.MULTILINE)
        cell_tags = {tag.strip().strip("'\"") for tag in tags.group(1).split(",")} if tags else set()
        if "illustrative" not in cell_tags:
            raise ValidationError(f"{relative}: executable code cells must be tagged illustrative")
        if "thebe" not in cell_tags:
            raise ValidationError(f"{relative}: executable code cells must opt in to browser execution")
    if "{code-cell}" in body and not cells:
        raise ValidationError(f"{relative}: malformed executable code cell")
    return len(cells)


def _validate_article_citations(relative: str, body: str, bibliography: set[str]) -> None:
    cited = set(re.findall(r"(?<![\w])@([A-Za-z][A-Za-z0-9_:-]*)", body))
    missing = sorted(cited - bibliography)
    if missing:
        raise ValidationError(f"{relative}: missing bibliography key(s): {', '.join(missing)}")


def validate_article(root: Path, path: Path, bibliography: set[str]) -> tuple[int, int]:
    relative = path.relative_to(root).as_posix()
    source = path.read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\s*\n(.*?)\n---\s*\n", source, re.DOTALL)
    if not frontmatter:
        raise ValidationError(f"{relative}: missing YAML frontmatter")
    metadata = frontmatter.group(1)
    for field in ("title", "description"):
        if not re.search(rf"^{field}:\s*\S", metadata, re.MULTILINE):
            raise ValidationError(f"{relative}: frontmatter requires a non-empty {field}")
    body = source[frontmatter.end():]
    if not re.search(r"^#\s+\S", body, re.MULTILINE):
        raise ValidationError(f"{relative}: article needs a top-level heading")
    links_checked = check_local_links(root, path, body)
    links_checked += _validate_article_figures(root, path, relative, body)
    cell_count = _validate_article_cells(relative, body)
    _validate_article_citations(relative, body, bibliography)
    return links_checked, cell_count


def _validate_articles(root: Path) -> tuple[int, int, int, dict[int, Path]]:
    article_paths = sorted(root.joinpath("articles").glob("*.md"))
    if not article_paths:
        raise ValidationError("no canonical MyST articles found")
    bibliography_paths = sorted(root.joinpath("articles").glob("*.bib"))
    if len(bibliography_paths) != 1:
        raise ValidationError("articles must declare exactly one local bibliography")
    bibliography_source = bibliography_paths[0].read_text(encoding="utf-8")
    bibliography = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", bibliography_source))
    links_checked = 0
    code_cell_count = 0
    for path in article_paths:
        article_links, article_cells = validate_article(root, path, bibliography)
        links_checked += article_links
        code_cell_count += article_cells
    toc_source = (root / "myst.yml").read_text(encoding="utf-8")
    toc_paths = re.findall(r"^\s+- file:\s*(articles/\S+\.md)\s*$", toc_source, re.MULTILINE)
    index_paths = re.findall(r"^\s+- file:\s*index\.md\s*$", toc_source, re.MULTILINE)
    if len(index_paths) != 1:
        raise ValidationError("myst.yml project.toc must list the publication index exactly once")
    article_relatives = {path.relative_to(root).as_posix() for path in article_paths}
    if len(toc_paths) != len(set(toc_paths)) or set(toc_paths) != article_relatives:
        raise ValidationError("myst.yml project.toc must list every canonical article exactly once")
    articles_by_sequence = {sequence: root / relative
                            for sequence, relative in enumerate(toc_paths, start=1)}
    if not articles_by_sequence:
        raise ValidationError("myst.yml project.toc must list the canonical articles")
    return len(article_paths), links_checked, code_cell_count, articles_by_sequence


def _validate_dispositions(root: Path, notebooks: list[Path],
                            articles_by_sequence: dict[int, Path]) -> int:
    path = root / "PUBLICATION-DISPOSITIONS.md"
    source = path.read_text(encoding="utf-8")
    links_checked = check_local_links(root, path, source)
    notebook_rows: dict[str, tuple[str, str]] = {}
    row_pattern = re.compile(
        r"^\|\s*\[[^\]]+\]\((notebooks/[^)]+\.ipynb)\)\s*\|\s*"
        r"(canonical article|supporting/source notebook)\s*\|\s*(.*?)\s*\|$"
    )
    for line in source.splitlines():
        match = row_pattern.match(line)
        if match:
            target, disposition, reader_cell = match.groups()
            if target in notebook_rows:
                raise ValidationError(f"{path.name}: duplicate notebook disposition for {target}")
            notebook_rows[target] = (disposition, reader_cell)

    expected_notebooks: set[str] = set()
    seen_sequences: set[int] = set()
    for notebook_path in notebooks:
        notebook = load_notebook(notebook_path)
        sequence = notebook["metadata"]["publication"].get("sequence")
        relative = notebook_path.relative_to(root).as_posix()
        if sequence is None:
            if relative != "notebooks/visual_intuition_atlas.ipynb":
                raise ValidationError(f"{relative}: public source notebook has no disposition sequence")
            expected_notebooks.add(relative)
            row = notebook_rows.get(relative)
            if row is None or row[0] != "supporting/source notebook":
                raise ValidationError(f"{path.name}: Visual Intuition Atlas must remain classified as a source notebook")
            continue
        expected_notebooks.add(relative)
        if sequence in seen_sequences:
            raise ValidationError(f"{relative}: duplicate notebook sequence {sequence}")
        seen_sequences.add(sequence)
        row = notebook_rows.get(relative)
        if row is None or row[0] != "canonical article":
            raise ValidationError(f"{path.name}: {relative} must have a canonical article disposition")
        targets = markdown_targets(row[1])
        article_targets = [target for target in targets if target.startswith("articles/") and target.endswith(".md")]
        article_path = articles_by_sequence.get(sequence)
        if (article_path is None or article_targets != [article_path.relative_to(root).as_posix()]):
            raise ValidationError(f"{path.name}: {relative} must point to its sequence-matched canonical article")

    if set(notebook_rows) != expected_notebooks:
        extra = sorted(set(notebook_rows) - expected_notebooks)
        missing = sorted(expected_notebooks - set(notebook_rows))
        raise ValidationError(f"{path.name}: notebook dispositions differ from publication inputs; missing={missing}, extra={extra}")
    if seen_sequences != set(articles_by_sequence):
        raise ValidationError(f"{path.name}: every numbered source notebook must have one canonical article")
    return links_checked


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


def _build_input_paths(root: Path) -> list[Path]:
    paths = []
    for name in BUILD_INPUTS:
        path = root / name
        if not path.is_file() or path.is_symlink():
            raise ValidationError(f"missing or unsafe build input: {name}")
        paths.append(path)
    return paths


def _validate_notebooks(root: Path) -> tuple[list[Path], int]:
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
    return notebooks, links_checked


def _validate_context_markdown(root: Path) -> int:
    links_checked = 0
    markdown_paths = sorted(root.joinpath("reference").rglob("*.md")) + [root / name for name in CONTEXT_FILES]
    for path in markdown_paths:
        if not path.is_file():
            raise ValidationError(f"missing publication context file: {path.relative_to(root)}")
        links_checked += check_local_links(root, path, path.read_text(encoding="utf-8"))
    return links_checked


def validate(root: Path) -> dict:
    paths = published_files(root) + _build_input_paths(root)
    paths.extend(root / name for name in CONTEXT_FILES)
    paths.sort(key=lambda path: path.relative_to(root).as_posix())
    allowed = {".ipynb", ".md", ".bib", ".svg", ".yml", ".json"}
    unexpected = [path.relative_to(root).as_posix() for path in paths if path.suffix not in allowed]
    if unexpected:
        raise ValidationError(f"unsupported publication input(s): {', '.join(unexpected)}")

    notebooks, links_checked = _validate_notebooks(root)
    links_checked += _validate_context_markdown(root)
    article_count, article_links, code_cell_count, articles_by_sequence = _validate_articles(root)
    links_checked += article_links
    links_checked += _validate_dispositions(root, notebooks, articles_by_sequence)

    return {
        "schema": SCHEMA,
        "coverage": ["articles/*.{md,bib,svg}", "notebooks/*.ipynb", "reference/**/*.md",
                     *BUILD_INPUTS, *CONTEXT_FILES],
        "contextChecked": list(CONTEXT_FILES),
        "sourceDigest": {"algorithm": "sha256-path-content-v1", "value": digest_paths(root, paths)},
        "fileCount": len(paths),
        "notebookCount": len(notebooks),
        "articleCount": article_count,
        "executableCellCount": code_cell_count,
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
