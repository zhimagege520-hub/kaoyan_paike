from __future__ import annotations

import unittest

import scheduler
from scripts.schedule_class_windows import class_window_matches, row_to_constraint
from scripts.window_utils import (
    SEASON_WINDOW_ID_TO_NAME,
    SEASON_WINDOW_ORDER,
    expanded_window_tokens,
    season_window_id_for_name,
    season_window_name_for_id,
)


class WindowUtilsTest(unittest.TestCase):
    def test_expanded_window_tokens_maps_ids_names_and_year_windows(self) -> None:
        self.assertEqual(SEASON_WINDOW_ORDER, ("寒假", "春季", "暑假", "秋季"))
        self.assertEqual(SEASON_WINDOW_ID_TO_NAME["WINDOW_SUMMER"], "暑假")
        self.assertEqual(season_window_name_for_id("WINDOW_AUTUMN"), "秋季")
        self.assertEqual(season_window_id_for_name("寒假"), "WINDOW_WINTER")

        tokens = expanded_window_tokens("WINDOW_SUMMER, 2026秋季；寒假")

        self.assertIn("WINDOW_SUMMER", tokens)
        self.assertIn("暑假", tokens)
        self.assertIn("2026秋季", tokens)
        self.assertIn("WINDOW_AUTUMN", tokens)
        self.assertIn("秋季", tokens)
        self.assertIn("WINDOW_WINTER", tokens)
        self.assertIn("寒假", tokens)

    def test_scheduler_reuses_shared_window_expansion(self) -> None:
        self.assertIs(scheduler.expanded_window_tokens, expanded_window_tokens)
        self.assertIn("WINDOW_SUMMER", scheduler.expanded_window_tokens("2026暑假"))

    def test_product_rule_matches_slot_with_only_year_window_id(self) -> None:
        slot = scheduler.TimeSlot(
            id="2026-07-01-AM-1",
            date="2026-07-01",
            period="AM",
            name="上午",
            order=1,
            schedule_window_id="2026暑假",
        )
        rule = scheduler.ScheduleRule(
            subject=None,
            stage=None,
            course_module=None,
            course_group=None,
            start_date=None,
            end_date=None,
            allowed_periods=None,
            allowed_weekdays=None,
            excluded_weekdays=None,
            block_hours=None,
            season_window_ids={"WINDOW_SUMMER"},
        )

        self.assertTrue(scheduler.slot_matches_schedule_rule(slot, rule))

    def test_class_window_constraint_matches_slot_by_season_name_or_id(self) -> None:
        slot = scheduler.TimeSlot(
            id="2026-07-01-AM-1",
            date="2026-07-01",
            period="AM",
            name="上午",
            order=1,
            schedule_window_id="2026暑假",
        )
        constraint = scheduler.ClassWindowConstraint(
            class_id="C1",
            start_date=None,
            start_period=None,
            end_date=None,
            end_period=None,
            schedule_window_id=None,
            season_window_id="WINDOW_SUMMER",
            season_name=None,
            room_ids=None,
        )

        self.assertTrue(scheduler.slot_matches_class_window_constraint(slot, constraint))

    def test_teacher_unavailability_matches_equivalent_window_tokens(self) -> None:
        slot = scheduler.TimeSlot(
            id="2026-07-01-AM-1",
            date="2026-07-01",
            period="AM",
            name="上午",
            order=1,
            schedule_window_id="2026暑假",
        )
        rule = scheduler.TeacherUnavailableRule(
            teacher_id="T1",
            start_date=None,
            end_date=None,
            weekdays=None,
            periods=None,
            schedule_window_ids={"2026年暑假"},
        )

        self.assertTrue(scheduler.slot_matches_teacher_unavailability(slot, rule))

    def test_class_window_filter_accepts_season_id_when_row_only_has_year_window(self) -> None:
        row = {
            "class_id": "C1",
            "schedule_window_id": "2026暑假",
            "season_window_id": "",
            "season_name": "",
            "schedule_window_name": "",
        }

        self.assertTrue(class_window_matches(row, None, {"WINDOW_SUMMER"}))
        self.assertTrue(class_window_matches(row, None, {"暑假"}))
        self.assertFalse(class_window_matches(row, None, {"WINDOW_AUTUMN"}))

    def test_class_window_row_to_constraint_preserves_falsey_values_and_common_separators(self) -> None:
        constraint = row_to_constraint(
            {
                "class_window_id": 0,
                "class_id": 0,
                "class_name": False,
                "product_id": 0,
                "schedule_window_id": 0,
                "season_window_id": False,
                "season_name": 0,
                "schedule_window_name": False,
                "earliest_date": "2026/7/1",
                "earliest_period": "上午",
                "latest_date": "2026.7.2",
                "latest_period": "晚上",
                "preferred_teaching_area_ids": "A1，A2",
                "preferred_room_ids": "R1；R2",
                "preferred_room_is_required": False,
                "notes": 0,
            }
        )

        self.assertEqual("0", constraint.class_window_id)
        self.assertEqual("0", constraint.class_id)
        self.assertEqual("False", constraint.class_name)
        self.assertEqual("0", constraint.product_id)
        self.assertEqual("0", constraint.schedule_window_id)
        self.assertEqual("False", constraint.season_window_id)
        self.assertEqual("0", constraint.season_name)
        self.assertEqual("False", constraint.schedule_window_name)
        self.assertEqual("2026-07-01", constraint.earliest_date)
        self.assertEqual("AM", constraint.earliest_period)
        self.assertEqual("2026-07-02", constraint.latest_date)
        self.assertEqual("EVENING", constraint.latest_period)
        self.assertEqual(frozenset({"A1", "A2"}), constraint.teaching_area_ids)
        self.assertEqual(frozenset({"R1", "R2"}), constraint.room_ids)
        self.assertFalse(constraint.preferred_room_is_required)
        self.assertEqual("0", constraint.notes)


if __name__ == "__main__":
    unittest.main()
