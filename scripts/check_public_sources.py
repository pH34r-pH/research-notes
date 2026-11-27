"""Read back declared public evidence, DOI records and publisher backlinks."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from http.client import HTTPException
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from claim_evidence import _unique_object, load_claims
from validate_publication import SHA, citation_keys, markdown_targets

CATALOG = "https://experiments.tyharbin.com/data/experiments.json"
RAW_GITHUB = "https://raw.githubusercontent.com"
NOTES_GITHUB = "https://github.com/pH34r-pH/research-notes/blob/main/"
HOSTS = {"raw.githubusercontent.com", "experiments.tyharbin.com", "tyharbin.com",
         "api.crossref.org", "aclanthology.org"}
MAX_BYTES = 2_000_000
ENTRY = re.compile(r"^@\w+\s*\{\s*([^,\s]+),", re.MULTILINE)
DOI = re.compile(r"10\.[0-9]{4,9}/[-._;()/:a-z0-9]+", re.IGNORECASE)


class Finding(ValueError):
    def __init__(self, status, detail):
        super().__init__(detail)
        self.status = status


class NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


class WebPage(HTMLParser):
    def __init__(self, body):
        super().__init__()
        self.links = set()
        self.canonical = None
        self.dois = set()
        self.feed(body.decode("utf-8"))

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.links.add(values["href"])
        if tag == "link" and values.get("rel") == "canonical":
            self.canonical = values.get("href")
        if tag == "meta" and values.get("name") == "citation_doi" and values.get("content"):
            self.dois.add(values["content"].lower())


def fetch(url):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc not in HOSTS or parsed.fragment:
        raise Finding("unconfirmed", "unapproved public source URL")
    request = Request(url, headers={"User-Agent": "ResearchNotes-SourceReadback/1.0"})
    try:
        with build_opener(NoRedirects()).open(request, timeout=8) as response:
            body = response.read(MAX_BYTES + 1)
            if response.status != 200 or len(body) > MAX_BYTES:
                raise Finding("unconfirmed", "public source response was incomplete or too large")
            return body
    except HTTPError as exc:
        status = "unavailable" if exc.code in (404, 410) else "unconfirmed"
        raise Finding(status, f"public source returned HTTP {exc.code}") from None
    except (TimeoutError, URLError, HTTPException):
        raise Finding("unconfirmed", "public source request did not complete") from None


def parsed_json(body):
    return json.loads(body, object_pairs_hook=_unique_object)


def require(condition, detail):
    if not condition:
        raise Finding("source-changed", detail)


def raw_github(url):
    return f"{RAW_GITHUB}{urlsplit(url).path.replace('/blob/', '/', 1)}"


def checked_experiment(claim, read):
    evidence = claim["evidence"]
    package_id = evidence["finalizationId"]
    require(package_id.encode() in read(raw_github(evidence["url"])),
            "pinned walkthrough lacks the finalization ID")
    catalog = parsed_json(read(CATALOG))
    require(catalog["schemaVersion"] == 2, "public catalog schema changed")
    records = [record for record in catalog["experiments"] if record["id"] == package_id]
    require(len(records) == 1, "catalog does not contain one exact finalization")
    entry, = records
    if entry["lifecycle"]["creativeWorkStatus"].lower() in {"retracted", "withdrawn"}:
        raise Finding("retracted", "public catalog reports a withdrawn or retracted package")
    require(entry["package"]["sha256"] == evidence["finalizationSha256"]
            and entry["detailUrl"] == urlsplit(evidence["readerUrl"]).path,
            "public catalog package or reader identity changed")
    require(package_id.encode() in read(evidence["readerUrl"]), "reader does not identify the exact finalization")
    backlink = f"https://tyharbin.com/articles/{Path(claim['passage']['path']).stem}/"
    require(any(row["url"] == backlink for row in entry["backlinks"]), "catalog no longer links the article")
    article = WebPage(read(backlink))
    require(article.canonical == backlink and evidence["readerUrl"] in article.links,
            "public article identity or reciprocal experiment link changed")
    return {"finalizationId": package_id, "packageSha256": entry["package"]["sha256"], "backlink": backlink}


def formal_backlink(record, passage, read):
    backlink = record["publicReference"]["researchNotes"]
    source_url, _, fragment = backlink.partition("#")
    require(source_url == NOTES_GITHUB + passage["path"] and fragment, "formal record no longer links the passage")
    markdown = read(raw_github(source_url)).decode("utf-8")
    heading = re.search(rf"^\({re.escape(passage['anchor'])}\)=\s*\n#+\s+([^\n]+)", markdown, re.MULTILINE)
    require(heading is not None, "formal backlink passage is missing")
    slug = re.sub(r"[^\w\- ]", "", heading[1].lower()).replace(" ", "-")
    require(fragment in (slug, passage["anchor"]), "formal backlink anchor changed")
    return backlink


def checked_formal(claim, read):
    evidence = claim["evidence"]
    proof = read(raw_github(evidence["url"]))
    require(hashlib.sha256(proof).hexdigest() == evidence["sourceSha256"], "pinned Lean source digest changed")
    pinned = parsed_json(read(raw_github(evidence["applicabilityUrl"])))
    current_url = raw_github(evidence["applicabilityUrl"]).replace(evidence["applicabilityRevision"], "main", 1)
    current = parsed_json(read(current_url))
    require(pinned["id"] == evidence["formalId"] and pinned["proof"]["sourceSha256"] == evidence["sourceSha256"]
            and pinned["proof"]["declaration"] == evidence["declaration"], "pinned applicability identifies another proof")
    require(all(pinned[key] == current[key] for key in ("id", "proof", "formalScope", "studyHandoff")),
            "current proof, premise or applicability differs from the pinned record")
    return {"formalId": pinned["id"], "sourceSha256": evidence["sourceSha256"],
            "backlink": formal_backlink(current, claim["passage"], read)}


def checked_document(claim, read):
    evidence = claim["evidence"]
    actual = hashlib.sha256(read(raw_github(evidence["url"]))).hexdigest()
    require(actual == evidence["sourceSha256"], "pinned source document digest changed")
    return {"sourceSha256": actual, "sourceUrl": evidence["url"]}


def bibliography_rows(path):
    source = path.read_text(encoding="utf-8")
    entries = list(ENTRY.finditer(source))
    for index, entry in enumerate(entries):
        end = entries[index + 1].start() if index + 1 < len(entries) else len(source)
        text = source[entry.end():end]
        doi = re.search(r"^\s*doi\s*=\s*\{([^}]+)\}", text, re.MULTILINE | re.IGNORECASE)
        url = re.search(r"^\s*url\s*=\s*\{([^}]+)\}", text, re.MULTILINE | re.IGNORECASE)
        yield entry[1], doi[1] if doi else None, url[1] if url else None


def checked_doi(doi, publisher, read):
    if doi is None or publisher is None or DOI.fullmatch(doi) is None:
        raise Finding("unconfirmed", "bibliography entry lacks a checked DOI and publisher URL")
    url = f"https://api.crossref.org/works/{quote(doi, safe='/')}"
    data = parsed_json(read(url))
    require(data["message-type"] == "work" and data["message"]["DOI"].lower() == doi.lower(),
            "Crossref returned a different DOI identity")
    updates = data["message"].get("updated-by", [])
    notices = [update["type"].lower() for update in updates]
    title = " ".join(data["message"].get("title", [])).lower()
    if "retraction" in notices or title.startswith("retracted:"):
        raise Finding("retracted", "Crossref reports a retraction")
    if notices:
        raise Finding("needs-review", "Crossref reports an editorial update")
    require(doi.lower() in WebPage(read(publisher)).dois, "publisher page advertises a different DOI identity")
    return {"doi": doi.lower(), "publisher": publisher, "crossrefUpdate": "none-reported"}


def check_entry(identity, check, *inputs):
    try:
        return {"id": identity, "status": "checked", **check(*inputs)}
    except Finding as exc:
        return {"id": identity, "status": exc.status, "reason": str(exc)}
    except (KeyError, IndexError, TypeError, AttributeError, ValueError):
        return {"id": identity, "status": "unconfirmed", "reason": "unexpected public source metadata"}


def article_citations(root):
    paths = {}
    for article in sorted((root / "articles").glob("*.md")):
        for key in citation_keys(article.read_text(encoding="utf-8")):
            paths.setdefault(key, []).append(article.relative_to(root).as_posix())
    return paths


def check_sources(root, read=fetch):
    claims = load_claims(root, markdown_targets)
    checks = {"lean": checked_formal, "compiled-experiment": checked_experiment, "source-document": checked_document}
    evidence = [
        {**check_entry(key, checks[claim["evidence"]["kind"]], claim, read),
         "passage": claim["passage"], "claimStatus": claim["status"]}
        for key, claim in claims.items()
    ]
    articles = article_citations(root)
    citations = [{**check_entry(key, checked_doi, doi, publisher, read), "citedBy": articles.get(key, [])}
                 for bib in sorted((root / "articles").glob("*.bib")) for key, doi, publisher in bibliography_rows(bib)]
    clear = bool(evidence) and bool(citations) and all(row["status"] == "checked" for row in evidence + citations)
    return {"status": "checked" if clear else "needs-review", "claims": evidence, "bibliography": citations}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--source-sha", default=os.environ.get("GITHUB_SHA"))
    args = parser.parse_args()
    try:
        report = check_sources(args.root)
        report["schema"] = "research-notes-public-source-readback/v1"
        report["checkedAt"] = datetime.now(timezone.utc).isoformat()
        if args.source_sha:
            if SHA.fullmatch(args.source_sha) is None:
                raise ValueError("the readback source SHA must be an exact Git commit")
            report["sourceSha"] = args.source_sha
        raw = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if args.receipt:
            args.receipt.parent.mkdir(parents=True, exist_ok=True)
            args.receipt.write_text(raw, encoding="utf-8")
        print(raw, end="")
    except (OSError, ValueError, TypeError) as exc:
        parser.exit(1, f"public source check failed: {exc}\n")
    if report["status"] != "checked":
        parser.exit(1, "one or more public evidence sources need review\n")


if __name__ == "__main__":
    main()
