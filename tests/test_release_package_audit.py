from __future__ import annotations

import unittest

from scripts.audit_release_package import REQUIRED_PATHS, audit_paths, forbidden_reason, normalize_path


class ReleasePackageAuditTest(unittest.TestCase):
    def test_required_release_paths_pass_without_private_files(self) -> None:
        self.assertEqual([], audit_paths(REQUIRED_PATHS))

    def test_release_audit_reports_missing_required_paths(self) -> None:
        paths = [path for path in REQUIRED_PATHS if path != "README.md"]

        self.assertIn("missing required file: README.md", audit_paths(paths))

    def test_release_audit_blocks_private_generated_and_secret_paths(self) -> None:
        paths = [
            *REQUIRED_PATHS,
            "data/classes.csv",
            "outputs/schedule.csv",
            "scripts/__pycache__/schedule_batch.cpython-313.pyc",
            ".env",
            "share/.DS_Store",
        ]

        issues = audit_paths(paths)

        self.assertTrue(any(issue.endswith("data/classes.csv") for issue in issues))
        self.assertTrue(any(issue.endswith("outputs/schedule.csv") for issue in issues))
        self.assertTrue(any(issue.endswith("scripts/__pycache__/schedule_batch.cpython-313.pyc") for issue in issues))
        self.assertTrue(any(issue.endswith(".env") for issue in issues))
        self.assertTrue(any(issue.endswith("share/.DS_Store") for issue in issues))

    def test_env_example_is_allowed_but_real_env_is_not(self) -> None:
        self.assertEqual("", forbidden_reason(".env.example"))
        self.assertNotEqual("", forbidden_reason(".env"))

    def test_normalize_path_uses_archive_style_slashes(self) -> None:
        self.assertEqual("foo/bar.csv", normalize_path("./foo/bar.csv"))
        self.assertEqual(".env", normalize_path("./.env"))


if __name__ == "__main__":
    unittest.main()
