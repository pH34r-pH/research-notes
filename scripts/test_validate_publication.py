import copy
import json
import tempfile
import unittest
from pathlib import Path

from validate_publication import ValidationError, validate


NOTEBOOK = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {"publication": {"question": "What is shown?", "sequence": 1,
                                    "exampleKind": "illustrative"}},
    "cells": [{"cell_type": "markdown", "metadata": {}, "source": "[term](../reference/glossary.md)"}],
}


class PublicationValidationTest(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
