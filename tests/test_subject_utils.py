from __future__ import annotations

import unittest

from scripts.subject_utils import (
    PUBLIC_SUBJECT_SORT_ORDER,
    PUBLIC_SUBJECTS_WITH_CHINESE,
    subject_sort_value,
)


class SubjectUtilsTest(unittest.TestCase):
    def test_public_subjects_with_chinese_are_shared(self) -> None:
        self.assertEqual(PUBLIC_SUBJECTS_WITH_CHINESE, frozenset({"英语", "政治", "数学", "语文"}))

    def test_public_subject_sort_order_is_shared(self) -> None:
        self.assertEqual(PUBLIC_SUBJECT_SORT_ORDER, {"数学": 0, "英语": 1, "政治": 2, "语文": 3})
        self.assertEqual(subject_sort_value(" 数学 "), 0)
        self.assertEqual(subject_sort_value("未知"), 99)


if __name__ == "__main__":
    unittest.main()
