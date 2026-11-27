import copy
import hashlib
import json
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

from check_public_sources import (
    CATALOG,
    NOTES_GITHUB,
    Finding,
    checked_source_link,
    check_entry,
    check_sources,
    checked_document,
    checked_doi,
    checked_experiment,
    checked_formal,
    fetch,
    raw_github,
)
from claim_evidence import load_claims
from validate_publication import markdown_targets

ROOT = Path(__file__).resolve().parents[1]
COMPILER = "historical-muon-optimizer-comparison"
FORMAL = "normalization-spectrum-local-derivative"
DOI = "10.18653/v1/2020.acl-main.420"
PUBLISHER = "https://aclanthology.org/2020.acl-main.420/"


class PublicSourceReadbackTests(unittest.TestCase):
    def setUp(self):
        self.claims = load_claims(ROOT, markdown_targets)
        self.experiment = copy.deepcopy(self.claims[COMPILER])
        self.formal = copy.deepcopy(self.claims[FORMAL])
        self.proof = b"synthetic proof input"
        self.formal["evidence"]["sourceSha256"] = hashlib.sha256(self.proof).hexdigest()
        self.sources = {}
        self.catalog_fixture()
        self.applicability_fixture()

    def catalog_fixture(self):
        evidence = self.experiment["evidence"]
        self.article = "https://tyharbin.com/articles/005-unit-hypersphere-anomaly/"
        self.catalog = {"schemaVersion": 2, "experiments": [{
            "id": evidence["finalizationId"],
            "detailUrl": "/" + evidence["readerUrl"].split("/", 3)[3],
            "package": {"sha256": evidence["finalizationSha256"]},
            "backlinks": [{"url": self.article}],
            "lifecycle": {"creativeWorkStatus": "Draft"},
        }]}
        self.sources[raw_github(evidence["url"])] = evidence["finalizationId"].encode()
        self.evaluator = b"synthetic archived evaluator"
        evidence["evaluatorSha256"] = hashlib.sha256(self.evaluator).hexdigest()
        self.sources[raw_github(evidence["evaluatorUrl"])] = self.evaluator
        self.sources[evidence["readerUrl"]] = evidence["finalizationId"].encode()
        self.sources[self.article] = (f'<link rel="canonical" href="{self.article}">'
                                      f'<a href="{evidence["readerUrl"]}">Experiment</a>').encode()

    def applicability_fixture(self):
        evidence = self.formal["evidence"]
        self.backlink = NOTES_GITHUB + self.formal["passage"]["path"]
        self.applicability = {
            "id": evidence["formalId"],
            "proof": {"sourceSha256": evidence["sourceSha256"], "declaration": evidence["declaration"]},
            "formalScope": {"premise": "nonzero"},
            "studyHandoff": {"applicability": "unmeasured"},
            "publicReference": {"researchNotes": self.backlink + "#frm-000133--normalization-spectrum"},
        }
        self.sources[raw_github(evidence["url"])] = self.proof
        self.sources[raw_github(self.backlink)] = (
            b"(frm-000133-normalization-spectrum)=\n## FRM-000133 \xe2\x80\x94 normalization spectrum\n"
        )

    def read(self, url):
        if url == CATALOG:
            return json.dumps(self.catalog).encode()
        return self.sources[url]

    def experiment_check(self):
        return check_entry(COMPILER, checked_experiment, self.experiment, self.read)

    def formal_check(self, current=None):
        evidence = self.formal["evidence"]
        url = raw_github(evidence["applicabilityUrl"])
        self.sources[url] = json.dumps(self.applicability).encode()
        current_url = url.replace(evidence["applicabilityRevision"], "main", 1)
        self.sources[current_url] = json.dumps(self.applicability if current is None else current).encode()
        return check_entry(FORMAL, checked_formal, self.formal, self.read)

    def doi_check(self, *, registered=DOI, updates=None, publisher_doi=DOI):
        self.sources[f"https://api.crossref.org/works/{DOI}"] = json.dumps({
            "message-type": "work", "message": {"DOI": registered, "updated-by": updates or []},
        }).encode()
        self.sources[PUBLISHER] = f'<meta name="citation_doi" content="{publisher_doi}">'.encode()
        return check_entry("fixture-citation", checked_doi, DOI, PUBLISHER, self.read)

    def test_catalog_requires_package_identity_and_reciprocal_backlink(self):
        self.assertEqual(self.experiment_check()["status"], "checked")
        self.sources[self.article] = f'<link rel="canonical" href="{self.article}">'.encode()
        self.assertIn("reciprocal", self.experiment_check()["reason"])
        self.catalog["experiments"][0]["package"]["sha256"] = "1" * 64
        self.assertIn("catalog package", self.experiment_check()["reason"])

    def test_withdrawn_catalog_entry_requires_review(self):
        self.catalog["experiments"][0]["lifecycle"]["creativeWorkStatus"] = "Withdrawn"
        self.assertEqual(self.experiment_check()["status"], "retracted")

    def test_changed_evaluator_is_not_admitted_with_the_same_package_id(self):
        self.sources[raw_github(self.experiment["evidence"]["evaluatorUrl"])] = b"changed evaluator"
        result = self.experiment_check()
        self.assertEqual(result["status"], "source-changed")
        self.assertIn("evaluator digest", result["reason"])

    def test_formal_additions_do_not_supersede_the_pinned_proof(self):
        current = {**self.applicability, "supportingDeclarations": ["fixture"]}
        self.assertEqual(self.formal_check(current)["status"], "checked")
        current["studyHandoff"] = {"applicability": "measured"}
        self.assertEqual(self.formal_check(current)["status"], "source-changed")
        self.sources[raw_github(self.backlink)] = b"no matching heading"
        self.assertIn("passage is missing", self.formal_check()["reason"])

    def test_doi_identity_checks_both_registry_and_publisher(self):
        self.assertEqual(self.doi_check(registered=DOI.upper())["crossrefUpdate"], "none-reported")
        self.assertEqual(self.doi_check(registered="10.9999/different")["status"], "source-changed")
        self.assertEqual(self.doi_check(publisher_doi="10.9999/different")["status"], "source-changed")

    def test_doi_notices_are_not_treated_as_clear(self):
        self.assertEqual(self.doi_check(updates=[{"type": "retraction"}])["status"], "retracted")
        self.assertEqual(self.doi_check(updates=[{"type": "correction"}])["status"], "needs-review")

    def test_readback_reports_affected_passages_on_source_failure(self):
        def unavailable(_):
            raise Finding("unavailable", "fixture response")

        report = check_sources(ROOT, unavailable)
        self.assertEqual(report["status"], "needs-review")
        formal = next(row for row in report["claims"] if row["id"] == FORMAL)
        self.assertEqual(formal["passage"], self.formal["passage"])
        cited = next(row for row in report["bibliography"] if row["id"] == "pimentel2020information")
        self.assertIn("articles/accessible-does-not-imply-used.md", cited["citedBy"])
        prose = next(row for row in report["linkedSources"] if row["id"] == "https://arxiv.org/abs/2410.01131v2")
        self.assertEqual(prose["status"], "unavailable")
        self.assertEqual(prose["citedBy"], ["articles/007-derive-before-training.md"])

    def test_arxiv_links_check_the_pinned_and_current_editions(self):
        paper = "https://arxiv.org/abs/2410.01131"
        url = paper + "v2"
        page = (f'<link rel="canonical" href="{paper}"><meta name="citation_arxiv_id" content="2410.01131">'
                f'<a href="{url}">Version</a><div class="submission-history"><strong>[v2]</strong></div>')
        self.sources[paper] = page.encode()
        self.sources[url] = page.encode()
        self.assertEqual(check_entry(url, checked_source_link, url, self.read)["version"], "v2")
        self.sources[paper] = page.replace("<strong>[v2]", "<strong>[v3]").encode()
        self.assertEqual(check_entry(url, checked_source_link, url, self.read)["status"], "source-changed")
        self.sources[paper] += b'<meta property="og:description" content="This paper has been withdrawn.">'
        self.assertEqual(check_entry(url, checked_source_link, url, self.read)["status"], "retracted")
        self.assertEqual(check_entry(paper, checked_source_link, paper, self.read)["status"], "source-changed")

    def test_inline_doi_requires_the_registered_destination_and_checks_notices(self):
        url = f"https://doi.org/{DOI}"
        crossref = f"https://api.crossref.org/works/{DOI}"
        record = {"message-type": "work", "message": {
            "DOI": DOI, "resource": {"primary": {"URL": PUBLISHER}},
        }}
        self.sources[crossref] = json.dumps(record).encode()
        self.sources[url] = PUBLISHER.encode()
        self.assertEqual(check_entry(url, checked_source_link, url, self.read)["registeredPublisher"], PUBLISHER)
        self.sources[url] = b"https://example.org/different"
        self.assertEqual(check_entry(url, checked_source_link, url, self.read)["status"], "source-changed")
        record["message"]["updated-by"] = [{"type": "retraction"}]
        self.sources[crossref] = json.dumps(record).encode()
        self.assertEqual(check_entry(url, checked_source_link, url, self.read)["status"], "retracted")

    def test_resolver_retains_the_destination_without_following_it(self):
        url = f"https://doi.org/{DOI}"
        with patch("check_public_sources.build_opener") as opener:
            open_url = opener.return_value.open
            open_url.side_effect = HTTPError(url, 302, "", {"Location": PUBLISHER}, None)
            self.assertEqual(fetch(url), PUBLISHER.encode())
            open_url.assert_called_once()

    def test_neurips_paper_checks_proceedings_identity_and_pdf_completeness(self):
        base = "https://papers.neurips.cc/paper_files/paper/2001"
        paper = "a" * 32
        abstract = f"{base}/hash/{paper}-Abstract.html"
        url = f"{base}/file/{paper}-Paper.pdf"
        self.sources[abstract] = (f'<meta name="citation_title" content="Fixture paper">'
                                  f'<meta name="citation_pdf_url" content="{url}">').encode()
        self.sources[url] = b"%PDF-1.5\n%%EOF\n"
        self.assertEqual(check_entry(url, checked_source_link, url, self.read)["proceedingsId"], paper)
        self.sources[url] = b"%PDF-1.5\n"
        self.assertEqual(check_entry(url, checked_source_link, url, self.read)["status"], "source-changed")
        self.sources[abstract] = self.sources[abstract].replace(paper.encode(), b"b" * 32)
        self.assertIn("different paper", check_entry(url, checked_source_link, url, self.read)["reason"])

    def test_inline_git_source_rejects_moving_revisions_and_broken_line_anchors(self):
        revision = "a" * 40
        url = f"https://github.com/example/research/blob/{revision}/README.md"
        self.sources[raw_github(url)] = b"First line\nSecond line\n"
        valid = url + "#L1-L2"
        self.assertEqual(check_entry(valid, checked_source_link, valid, self.read)["revision"], revision)
        for broken in (url + "#L3", url.replace(revision, "main")):
            self.assertEqual(check_entry(broken, checked_source_link, broken, self.read)["status"], "source-changed")
        unknown = "https://example.org/new-source"
        self.assertEqual(check_entry(unknown, checked_source_link, unknown, self.read)["status"], "unconfirmed")

    def test_pinned_document_digest_distinguishes_changed_source_from_unverified_empirics(self):
        record = copy.deepcopy(self.claims["unit-recurrence-frozen-endpoint"])
        document = b"synthetic preserved account"
        record["evidence"]["sourceSha256"] = hashlib.sha256(document).hexdigest()
        self.sources[raw_github(record["evidence"]["url"])] = document
        with patch("check_public_sources.load_claims", return_value={record["id"]: record}):
            report = check_sources(ROOT, self.read)
        self.assertEqual(report["claims"][0]["status"], "checked")
        self.assertEqual(report["claims"][0]["claimStatus"], "empirical-evidence-unverified")
        changed = check_entry(record["id"], checked_document, record, lambda _: b"changed fixture")
        self.assertEqual(changed["status"], "source-changed")

    def test_missing_and_transient_http_statuses_remain_distinct(self):
        url = "https://aclanthology.org/fixture/"
        for code, expected in ((404, "unavailable"), (429, "unconfirmed"), (503, "unconfirmed")):
            with self.subTest(code=code), patch("check_public_sources.build_opener") as opener:
                opener.return_value.open.side_effect = HTTPError(url, code, "", {}, None)
                row = check_entry("fixture-http", fetch, url)
                self.assertEqual(row["status"], expected)
