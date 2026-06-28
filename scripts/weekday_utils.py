from __future__ import annotations

import re
from datetime import date as Date
from typing import Any, Optional, Set

from scripts.field_utils import normalize_text


WEEKDAY_LABELS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
MONDAY = 0
SUNDAY = 6
WEEKDAY_ALIASES = {
    "0": 0,
    "1": 0,
    "MON": 0,
    "MONDAY": 0,
    "周一": 0,
    "星期一": 0,
    "一": 0,
    "2": 1,
    "TUE": 1,
    "TUESDAY": 1,
    "周二": 1,
    "星期二": 1,
    "二": 1,
    "3": 2,
    "WED": 2,
    "WEDNESDAY": 2,
    "周三": 2,
    "星期三": 2,
    "三": 2,
    "4": 3,
    "THU": 3,
    "THURSDAY": 3,
    "周四": 3,
    "星期四": 3,
    "四": 3,
    "5": 4,
    "FRI": 4,
    "FRIDAY": 4,
    "周五": 4,
    "星期五": 4,
    "五": 4,
    "6": 5,
    "SAT": 5,
    "SATURDAY": 5,
    "周六": 5,
    "星期六": 5,
    "六": 5,
    "7": 6,
    "SUN": 6,
    "SUNDAY": 6,
    "周日": 6,
    "周天": 6,
    "星期日": 6,
    "星期天": 6,
    "日": 6,
    "天": 6,
}


def normalize_weekday(value: Any) -> Optional[int]:
    text = normalize_text(value)
    if not text:
        return None
    return WEEKDAY_ALIASES.get(text.upper())


def split_weekday_values(values: Any) -> list[str]:
    if values is None:
        return []
    if isinstance(values, str):
        return [item.strip() for item in re.split(r"[|,，;；]+", values) if item.strip()]
    return [normalize_text(item) for item in values if normalize_text(item)]


def parse_weekday_set(values: Any, label: str = "星期") -> Optional[Set[int]]:
    weekdays = split_weekday_values(values)
    if not weekdays:
        return None

    normalized: Set[int] = set()
    for weekday in weekdays:
        value = normalize_weekday(weekday)
        if value is None:
            raise ValueError(f"{label} 包含不支持的星期 {weekday}")
        normalized.add(value)
    return normalized


def weekday_label_for_index(weekday: int) -> str:
    return WEEKDAY_LABELS[weekday]


def weekday_label_for_date(value: Date | str) -> str:
    day = Date.fromisoformat(value) if isinstance(value, str) else value
    return weekday_label_for_index(day.weekday())
