import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from claim_evidence import RECORD, load_claims, review_impact
from validate_publication import (
    ValidationError,
    _validate_article_relations,
    markdown_targets,
    validate,
)

NOTEBOOK = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {"publication": {"question": "What is shown?", "sequence": 1,
                                    "exampleKind": "illustrative"}},
    "cells": [{"cell_type": "markdown", "metadata": {}, "source": "[term](../reference/glossary.md)"}],
}


class PublicationValidationTest(unittest.TestCase):
    def _pilot_claims(self, root: Path) -> dict:
        published = Path(__file__).resolve().parents[1]
        document = json.loads((published / RECORD).read_text(encoding="utf-8"))
        document["claims"] = document["claims"][:2]
        for path in {row["passage"]["path"] for row in document["claims"]}:
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(published / path, target)
        (root / RECORD).write_text(json.dumps(document), encoding="utf-8")
        return document

    def test_all_articles_are_covered_and_reported_evidence_is_marked(self):
        receipt = validate(Path(__file__).resolve().parents[1])
        self.assertIn(RECORD, receipt["coverage"])
        self.assertGreaterEqual(receipt["claimEvidence"]["validatedClaims"], receipt["articleCount"])
        self.assertEqual(receipt["claimEvidence"]["annotatedArticles"], receipt["articleCount"])
        self.assertEqual(receipt["claimEvidence"]["unannotatedArticles"], 0)
        self.assertGreater(receipt["claimEvidence"]["unverifiedEmpiricalClaims"], 0)

    def test_coverage_and_empirical_status_cannot_be_silently_removed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            record = root / RECORD
            document = json.loads(record.read_text(encoding="utf-8"))
            article = root / "articles/sample.md"
            original = article.read_text(encoding="utf-8")
            article.write_text(original.replace("[Claim evidence record](../reference/claim-evidence.json).", ""),
                               encoding="utf-8")
            record.unlink()
            with self.assertRaisesRegex(ValidationError, "missing article claim records: articles/sample.md"):
                validate(root)
            article.write_text(original, encoding="utf-8")
            document["claims"][0].update({"kind": "observation", "status": "documented"})
            record.write_text(json.dumps(document), encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "invalid status for a documented claim"):
                validate(root)

    def test_claim_contract_rejects_missing_premise_moving_proof_and_unlinked_experiment(self):
        for case, error in (
            ("premise", "nonzero-input premise"), ("proof", "URL pinned"),
            ("proof-digest", "Lean declaration"),
            ("experiment-link", "passage must link"), ("supersession", "unknown superseded claim"),
        ):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                document = self._pilot_claims(root)
                muon, formal = document["claims"]
                if case == "premise":
                    formal["assumptions"].remove("nonzero-input")
                elif case == "proof":
                    evidence = formal["evidence"]
                    evidence["url"] = evidence["url"].replace(evidence["revision"], "main")
                elif case == "proof-digest":
                    formal["evidence"].pop("sourceSha256")
                elif case == "experiment-link":
                    page = root / muon["passage"]["path"]
                    source = page.read_text(encoding="utf-8")
                    page.write_text(source.replace(muon["evidence"]["readerUrl"], "https://example.org/"),
                                    encoding="utf-8")
                else:
                    muon["supersedes"] = ["unknown-claim"]
                (root / RECORD).write_text(json.dumps(document), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, error):
                    load_claims(root, markdown_targets)

    def test_impact_compares_proof_digest_to_proof_digest(self):
        published = Path(__file__).resolve().parents[1]
        claims = load_claims(published, markdown_targets)
        formal = claims["normalization-spectrum-local-derivative"]["evidence"]
        self.assertEqual(review_impact(claims, formal["formalId"], formal["sourceSha256"]), [])
        affected = review_impact(claims, formal["formalId"], "1" * 64)
        self.assertEqual([row["claimId"] for row in affected], ["normalization-spectrum-local-derivative"])
        self.assertEqual(affected[0]["retainedIdentity"], formal["sourceSha256"])

    def test_impact_reports_when_the_pinned_evaluator_changes(self):
        published = Path(__file__).resolve().parents[1]
        claims = load_claims(published, markdown_targets)
        claim = claims["historical-muon-optimizer-comparison"]
        evaluator = claim["evidence"]
        self.assertEqual(review_impact(claims, evaluator["evaluatorUrl"], evaluator["evaluatorSha256"]), [])
        affected = review_impact(claims, evaluator["evaluatorUrl"], "1" * 64)
        self.assertEqual([row["passage"] for row in affected], [claim["passage"]])
        self.assertEqual(affected[0]["retainedIdentity"], evaluator["evaluatorSha256"])

    def test_synthetic_successor_keeps_history_and_reports_only_affected_passage(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document = self._pilot_claims(root)
            original = document["claims"][0]
            successor = copy.deepcopy(original)
            successor["id"] = "synthetic-muon-follow-up"
            successor["supersedes"] = [original["id"]]
            successor["passage"]["anchor"] = "synthetic-muon-follow-up"
            new_revision = "a" * 40
            successor["evidence"]["revision"] = new_revision
            for field in ("url", "evaluatorUrl"):
                successor["evidence"][field] = successor["evidence"][field].replace(
                    original["evidence"]["revision"], new_revision,
                )
            page = root / successor["passage"]["path"]
            historical = page.read_text(encoding="utf-8")
            with page.open("a", encoding="utf-8") as handle:
                handle.write("\n(synthetic-muon-follow-up)=\n## Synthetic successor\n\n"
                             f"[Evidence]({successor['evidence']['url']})\n"
                             f"[Package]({successor['evidence']['readerUrl']})\n"
                             f"[Evaluator]({successor['evidence']['evaluatorUrl']})\n"
                             "[Claim record](../reference/claim-evidence.json)\n")
            document["claims"].append(successor)
            (root / RECORD).write_text(json.dumps(document), encoding="utf-8")
            claims = load_claims(root, markdown_targets)
            self.assertEqual(claims[original["id"]], original)
            self.assertTrue(page.read_text(encoding="utf-8").startswith(historical))
            affected = review_impact(claims, original["evidence"]["finalizationId"], new_revision)
            self.assertEqual([item["claimId"] for item in affected], [original["id"]])

    def test_article_relationships_and_preserved_notebook_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            article = root / 'articles/sample.md'
            original = article.read_text(encoding='utf-8')
            for metadata, error in [
                ('depends_on: [missing]', 'unknown article prerequisite'),
                ('depends_on: [sample]', 'cycle'),
                ('depends_on: [sample, sample]', 'duplicate prerequisite'),
                ('source_notebook: ../001', 'invalid source_notebook'),
                ('milestone: "002"\nsource_notebook: 001', 'identity disagree'),
                ('milestone: "001"\nsource_notebook: absent', 'source_notebook is missing'),
            ]:
                article.write_text(original.replace('title:', metadata + '\ntitle:', 1), encoding='utf-8')
                with self.subTest(metadata=metadata), self.assertRaisesRegex(ValidationError, error):
                    _validate_article_relations(root, [article])
            notebook = root / 'notebooks/001.ipynb'
            before = notebook.read_bytes()
            article.write_text(original.replace('title:', 'milestone: "001"\nsource_notebook: 001\ntitle:', 1), encoding='utf-8')
            _validate_article_relations(root, [article])
            self.assertEqual(before, notebook.read_bytes())

    def add_document_claim(self, root: Path, article_path: str) -> None:
        slug = Path(article_path).stem
        evidence = {
            "kind": "source-document", "repository": "pH34r-pH/research-notes",
            "revision": "b" * 40, "sourceSha256": "c" * 64,
            "url": f"https://github.com/pH34r-pH/research-notes/blob/{'b' * 40}/{article_path}",
        }
        path = root / RECORD
        document = (json.loads(path.read_text(encoding="utf-8")) if path.exists()
                    else {"schema": "research-notes-claim-evidence/v1", "claims": []})
        document["claims"].append({
            "id": slug, "kind": "limitation", "status": "documented", "statement": "Fixture scope.",
            "passage": {"path": article_path, "anchor": slug}, "evidence": evidence,
            "assumptions": ["fixture"], "limitations": ["illustrative"], "supersedes": [],
        })
        path.write_text(json.dumps(document), encoding="utf-8")
        with (root / article_path).open("a", encoding="utf-8") as handle:
            handle.write(f"\n({slug})=\n## Scope\n\n[Source]({evidence['url']}) "
                         "[Claim evidence record](../reference/claim-evidence.json).\n")

    def repository(self, directory: str) -> Path:
        root = Path(directory)
        (root / "notebooks").mkdir()
        (root / "reference").mkdir()
        (root / "reference/glossary.md").write_text("# Glossary\n", encoding="utf-8")
        (root / "articles").mkdir()
        (root / "articles/figure.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>\n", encoding="utf-8")
        (root / "articles/references.bib").write_text("@article{sample2026, title={A title}}\n", encoding="utf-8")
        (root / "articles/sample.md").write_text(
            "---\ntitle: Sample article\ndescription: A test article.\nsequence: 1\n---\n"
            "# Sample article\n\n"
            "```{figure} ./figure.svg\n:alt: Static figure\nCaption.\n```\n\n"
            "```{code-cell} python\n:tags: [illustrative, thebe]\n\nprint('example')\n```\n\n"
            "A citation [@sample2026].\n",
            encoding="utf-8",
        )
        (root / "myst.yml").write_text(
            "version: 1\nproject:\n  toc:\n    - file: index.md\n    - file: articles/sample.md\n", encoding="utf-8"
        )
        (root / "package.json").write_text("{}\n", encoding="utf-8")
        (root / "package-lock.json").write_text("{}\n", encoding="utf-8")
        (root / "README.md").write_text("[notes](notebooks/001.ipynb)\n", encoding="utf-8")
        (root / "CHRONOLOGY.md").write_text("[reference](reference/glossary.md)\n", encoding="utf-8")
        (root / "PUBLICATION-DISPOSITIONS.md").write_text(
            "| Source | Disposition | Reader page |\n"
            "| --- | --- | --- |\n"
            "| [001](notebooks/001.ipynb) | canonical article | [Sample](articles/sample.md) |\n",
            encoding="utf-8",
        )
        (root / "index.md").write_text("[Start with the article](articles/sample.md)\n", encoding="utf-8")
        (root / "notebooks/001.ipynb").write_text(json.dumps(NOTEBOOK), encoding="utf-8")
        self.add_document_claim(root, "articles/sample.md")
        return root

    def test_receipt_covers_consumer_inputs_and_is_deterministic(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            first = validate(root)
            second = validate(root)
            self.assertEqual(first, second)
            self.assertEqual(first["schema"], "research-notes-publication-validation/v2")
            self.assertEqual(first["notebookCount"], 1)
            self.assertEqual(first["articleCount"], 1)
            self.assertEqual(first["executableCellCount"], 1)
            self.assertIn("package-lock.json", first["coverage"])
            self.assertIn("PUBLICATION-DISPOSITIONS.md", first["coverage"])
            self.assertIn("index.md", first["coverage"])
            self.assertIn("index.md", first["contextChecked"])
            self.assertEqual(len(first["sourceDigest"]["value"]), 64)

    def test_articles_fail_closed_on_missing_figures_and_unlabeled_cells(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            source = (root / "articles/sample.md").read_text(encoding="utf-8")
            (root / "articles/sample.md").write_text(source.replace("figure.svg", "missing.svg"), encoding="utf-8")
            with self.assertRaises(ValidationError):
                validate(root)
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            source = (root / "articles/sample.md").read_text(encoding="utf-8")
            (root / "articles/sample.md").write_text(source.replace("illustrative, thebe", "thebe"), encoding="utf-8")
            with self.assertRaises(ValidationError):
                validate(root)

    def test_model_instrument_can_replace_an_uninformative_static_figure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            source = (root / "articles/sample.md").read_text(encoding="utf-8")
            source = source.replace(
                "sequence: 1\n",
                "sequence: 1\nmodel_focus: representation\nmodel_variant: baseline\n",
            )
            source = source.replace(
                "```{figure} ./figure.svg\n:alt: Static figure\nCaption.\n```\n\n",
                "",
            )
            (root / "articles/sample.md").write_text(source, encoding="utf-8")
            receipt = validate(root)
            self.assertEqual(receipt["articleCount"], 1)

    def test_article_without_static_or_model_visualization_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            source = (root / "articles/sample.md").read_text(encoding="utf-8")
            source = source.replace(
                "```{figure} ./figure.svg\n:alt: Static figure\nCaption.\n```\n\n",
                "",
            )
            (root / "articles/sample.md").write_text(source, encoding="utf-8")
            with self.assertRaises(ValidationError):
                validate(root)

    def test_missing_link_and_invalid_metadata_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            (root / "reference/glossary.md").unlink()
            with self.assertRaises(ValidationError):
                validate(root)

    def test_notebook_disposition_must_point_to_sequence_matched_article(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            source = (root / "PUBLICATION-DISPOSITIONS.md").read_text(encoding="utf-8")
            (root / "PUBLICATION-DISPOSITIONS.md").write_text(
                source.replace("articles/sample.md", "articles/missing.md"), encoding="utf-8"
            )
            with self.assertRaises(ValidationError):
                validate(root)
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            notebook = copy.deepcopy(NOTEBOOK)
            notebook["metadata"]["publication"]["exampleKind"] = "benchmark"
            (root / "notebooks/001.ipynb").write_text(json.dumps(notebook), encoding="utf-8")
            with self.assertRaises(ValidationError):
                validate(root)

    def test_standalone_article_requires_explicit_matching_disposition(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            (root / "articles/essay.md").write_text(
                "---\ntitle: Essay\ndescription: A standalone essay.\narticle_kind: essay\n---\n"
                "# Essay\n\n```{figure} ./figure.svg\n:alt: Example.\nCaption.\n```\n", encoding="utf-8")
            with (root / "myst.yml").open("a", encoding="utf-8") as handle:
                handle.write("    - file: articles/essay.md\n")
            with self.assertRaisesRegex(ValidationError, "matching public disposition"):
                validate(root)
            with (root / "PUBLICATION-DISPOSITIONS.md").open("a", encoding="utf-8") as handle:
                handle.write("| [Essay](articles/essay.md) | essay | Standalone article |\n")
            self.add_document_claim(root, "articles/essay.md")
            self.assertEqual(validate(root)["articleCount"], 2)


if __name__ == "__main__":
    unittest.main()
