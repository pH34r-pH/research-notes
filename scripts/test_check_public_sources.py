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
    check_entry,
    check_sources,
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
        self.experiment = self.claims[COMPILER]
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

    def test_missing_and_transient_http_statuses_remain_distinct(self):
        url = "https://aclanthology.org/fixture/"
        for code, expected in ((404, "unavailable"), (429, "unconfirmed"), (503, "unconfirmed")):
            with self.subTest(code=code), patch("check_public_sources.build_opener") as opener:
                opener.return_value.open.side_effect = HTTPError(url, code, "", {}, None)
                row = check_entry("fixture-http", fetch, url)
                self.assertEqual(row["status"], expected)
