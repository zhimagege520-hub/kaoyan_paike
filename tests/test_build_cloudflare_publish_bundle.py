from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import build_cloudflare_publish_bundle as bundle
from scripts.csv_utils import read_csv_rows


class BuildCloudflarePublishBundleTest(unittest.TestCase):
    def test_write_coverage_gap_summary_uses_shared_csv_format(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "coverage_gaps.csv"
            bundle.write_coverage_gap_summary(
                path,
                [
                    {
                        "class_id": "C1",
                        "class_name": "测试班",
                        "sub_product": "无忧",
                        "subject": "英语",
                        "suite_code": "1001",
                        "expected_hours": 4.0,
                        "scheduled_hours": 2.0,
                        "gap_hours": 2.0,
                        "ignored": "extra",
                    }
                ],
            )

            self.assertTrue(path.read_bytes().startswith(b"\xef\xbb\xbf"))
            text = path.read_text(encoding="utf-8-sig")
            rows = read_csv_rows(path)

        self.assertEqual(text.splitlines()[0], ",".join(bundle.COVERAGE_GAP_FIELDNAMES))
        self.assertEqual(rows[0]["class_id"], "C1")
        self.assertEqual(rows[0]["gap_hours"], "2.0")
        self.assertNotIn("ignored", rows[0])


if __name__ == "__main__":
    unittest.main()
