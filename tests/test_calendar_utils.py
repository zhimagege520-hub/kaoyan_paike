from __future__ import annotations

import unittest
from datetime import date as Date

from scripts.calendar_utils import (
    date_range,
    date_range_values,
    iso_week_key,
    iter_week_start_dates,
    week_dates,
    week_display_label,
    week_range,
    week_start,
    week_start_date,
    week_start_from_iso_key,
)


class CalendarUtilsTest(unittest.TestCase):
    def test_date_ranges_expand_inclusive_iso_dates(self) -> None:
        self.assertEqual(date_range("2026-07-01", "2026-07-03"), ["2026-07-01", "2026-07-02", "2026-07-03"])
        self.assertEqual(date_range_values("2026-07-01", "2026-07-03"), {"2026-07-01", "2026-07-02", "2026-07-03"})

    def test_week_helpers_use_monday_based_business_weeks(self) -> None:
        self.assertEqual(week_start("2026-07-05"), "2026-06-29")
        self.assertEqual(week_start_date(Date(2026, 7, 5)), Date(2026, 6, 29))
        self.assertEqual(
            week_dates("2026-06-29"),
            [
                "2026-06-29",
                "2026-06-30",
                "2026-07-01",
                "2026-07-02",
                "2026-07-03",
                "2026-07-04",
                "2026-07-05",
            ],
        )
        self.assertEqual(week_range("2026-07-01", "2026-07-14"), ["2026-06-29", "2026-07-06", "2026-07-13"])
        self.assertEqual(list(iter_week_start_dates("2026-07-01", "2026-07-14")), [Date(2026, 6, 29), Date(2026, 7, 6), Date(2026, 7, 13)])

    def test_iso_week_helpers_share_display_and_key_rules(self) -> None:
        self.assertEqual(iso_week_key("2026-07-05"), (2026, 27))
        self.assertEqual(week_start_from_iso_key((2026, 27)), Date(2026, 6, 29))
        self.assertEqual(week_display_label("2026-06-29"), "2026年第27周(2026-06-29起)")


if __name__ == "__main__":
    unittest.main()
