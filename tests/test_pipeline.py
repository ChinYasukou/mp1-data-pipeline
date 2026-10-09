import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src import process_data, save_data, validate_dataframe


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class DataValidatorTests(unittest.TestCase):
    def test_validate_dataframe_removes_invalid_numeric_rows(self):
        dataframe = pd.DataFrame(
            {
                "name": ["valid", "invalid", "missing"],
                "rating": ["42", "not-a-number", None],
            }
        )

        with self.assertLogs("src.data_validator", level="WARNING"):
            result = validate_dataframe(
                dataframe,
                required_columns=["name", "rating"],
                numeric_columns=["rating"],
            )

        self.assertEqual(result["name"].tolist(), ["valid", "missing"])
        self.assertTrue(pd.api.types.is_numeric_dtype(result["rating"]))

    def test_validate_dataframe_rejects_missing_required_column(self):
        dataframe = pd.DataFrame({"name": ["record"]})

        with self.assertLogs("src.data_validator", level="ERROR"):
            with self.assertRaisesRegex(ValueError, "rating"):
                validate_dataframe(
                    dataframe,
                    required_columns=["name", "rating"],
                    numeric_columns=["rating"],
                )


class ProcessingTests(unittest.TestCase):
    def test_process_data_applies_enabled_steps(self):
        dataframe = pd.DataFrame(
            {
                "rating": [10, 10, 11, 12, 13, 100, None],
                "name": ["A", "A", "B", "C", "D", "E", "F"],
            }
        )
        config = {
            "processing": {
                "remove_duplicates": True,
                "missing": {"enabled": True, "axis": "rows"},
                "outliers": {
                    "enabled": True,
                    "columns": ["rating"],
                    "method": "iqr",
                    "threshold": 1.5,
                },
            }
        }

        result = process_data(dataframe, config)

        self.assertEqual(result["name"].tolist(), ["A", "B", "C", "D"])


class OutputTests(unittest.TestCase):
    def test_save_data_creates_parent_directory(self):
        dataframe = pd.DataFrame({"value": [1, 2]})

        with tempfile.TemporaryDirectory() as directory:
            output_path = Path(directory) / "nested" / "clean.csv"
            result = save_data(dataframe, output_path)

            self.assertEqual(result, output_path)
            self.assertTrue(output_path.is_file())
            saved = pd.read_csv(output_path)

        self.assertEqual(saved["value"].tolist(), [1, 2])


class PipelineIntegrationTests(unittest.TestCase):
    def test_sample_pipeline_produces_expected_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output_path = Path(directory) / "clean.csv"
            result = subprocess.run(
                [
                    sys.executable,
                    str(PROJECT_ROOT / "pipeline.py"),
                    "--input",
                    str(PROJECT_ROOT / "fixtures" / "sample_data.csv"),
                    "--output",
                    str(output_path),
                    "--config",
                    str(PROJECT_ROOT / "config" / "config.yaml"),
                    "--verbose",
                ],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Validation complete: 100", result.stderr)
            self.assertIn("Processing complete: 98", result.stderr)
            self.assertIn("'rows_after': 92", result.stdout)
            cleaned = pd.read_csv(output_path)

        self.assertEqual(cleaned.shape, (92, 5))


if __name__ == "__main__":
    unittest.main()
