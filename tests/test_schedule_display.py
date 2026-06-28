from __future__ import annotations

import unittest

from scripts.schedule_display import date_range, week_dates, week_start, weekday_label


class ScheduleDisplayTest(unittest.TestCase):
    def test_calendar_helpers_use_current_display_conventions(self) -> None:
        self.assertEqual(weekday_label("2026-07-01"), "周三")
        self.assertEqual(date_range("2026-07-01", "2026-07-03"), ["2026-07-01", "2026-07-02", "2026-07-03"])
        self.assertEqual(week_start("2026-07-05"), "2026-06-29")
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


if __name__ == "__main__":
    unittest.main()
