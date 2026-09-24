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
        (root / "README.md").write_text("[notes](notebooks/001.ipynb)\n", encoding="utf-8")
        (root / "CHRONOLOGY.md").write_text("[reference](reference/glossary.md)\n", encoding="utf-8")
        (root / "notebooks/001.ipynb").write_text(json.dumps(NOTEBOOK), encoding="utf-8")
        return root

    def test_receipt_covers_consumer_inputs_and_is_deterministic(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            first = validate(root)
            second = validate(root)
            self.assertEqual(first, second)
            self.assertEqual(first["schema"], "research-notes-publication-validation/v1")
            self.assertEqual(first["notebookCount"], 1)
            self.assertEqual(len(first["sourceDigest"]["value"]), 64)

    def test_missing_link_and_invalid_metadata_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            (root / "reference/glossary.md").unlink()
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
