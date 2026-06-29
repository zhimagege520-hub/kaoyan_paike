from __future__ import annotations

from datetime import date
import unittest

import scheduler
from business_class_import import weekday_name
from generate_time_slots import parse_weekdays
from scripts.weekday_utils import (
    SUNDAY,
    WEEKDAY_LABELS,
    normalize_weekday,
    parse_weekday_set,
    weekday_label_for_date,
    weekday_label_for_index,
)


class WeekdayUtilsTest(unittest.TestCase):
    def test_normalize_weekday_accepts_template_cli_and_chinese_aliases(self) -> None:
        self.assertEqual(normalize_weekday("0"), 0)
        self.assertEqual(normalize_weekday("1"), 0)
        self.assertEqual(normalize_weekday("mon"), 0)
        self.assertEqual(normalize_weekday("星期三"), 2)
        self.assertEqual(normalize_weekday("周天"), SUNDAY)
        self.assertEqual(normalize_weekday("7"), SUNDAY)
        self.assertIsNone(normalize_weekday(""))

    def test_parse_weekday_set_accepts_common_separators(self) -> None:
        self.assertEqual(parse_weekday_set("Mon,周三|星期天；六", "测试"), {0, 2, 5, 6})
        self.assertEqual(parse_weekday_set(["周一", "Sun"], "测试"), {0, 6})
        self.assertIsNone(parse_weekday_set("", "测试"))

    def test_parse_weekday_set_raises_with_label(self) -> None:
        with self.assertRaisesRegex(ValueError, "产品/allowed_weekdays 包含不支持的星期 Funday"):
            parse_weekday_set("Funday", "产品/allowed_weekdays")

    def test_existing_entrypoints_reuse_shared_weekday_rules(self) -> None:
        self.assertEqual(parse_weekdays("Sun,Mon"), {0, 6})
        self.assertEqual(scheduler.parse_weekday_set("周一|Sun", "排课规则"), {0, 6})
        self.assertEqual(weekday_name(date(2026, 7, 1)), "周三")

    def test_weekday_labels_are_shared_for_dates_and_indexes(self) -> None:
        self.assertEqual(WEEKDAY_LABELS, ["周一", "周二", "周三", "周四", "周五", "周六", "周日"])
        self.assertEqual(weekday_label_for_index(0), "周一")
        self.assertEqual(weekday_label_for_date("2026-07-01"), "周三")
        self.assertEqual(weekday_label_for_date(date(2026, 7, 5)), "周日")


if __name__ == "__main__":
    unittest.main()
