from __future__ import annotations

import re
from typing import Any, Set

from scripts.field_utils import normalize_text, split_delimited_values


SEASON_WINDOW_ID_TO_NAME = {
    "WINDOW_WINTER": "寒假",
    "WINDOW_SPRING": "春季",
    "WINDOW_SUMMER": "暑假",
    "WINDOW_AUTUMN": "秋季",
}
SEASON_WINDOW_ORDER = tuple(SEASON_WINDOW_ID_TO_NAME.values())
SEASON_WINDOW_NAME_TO_ID = {name: window_id for window_id, name in SEASON_WINDOW_ID_TO_NAME.items()}
SEASON_WINDOW_DEFAULTS = {
    "寒假": {
        "season_window_id": "WINDOW_WINTER",
        "start_month": 1,
        "end_month": 2,
        "blocked_weekdays": ["周日"],
    },
    "春季": {
        "season_window_id": "WINDOW_SPRING",
        "start_month": 3,
        "end_month": 6,
        "blocked_weekdays": ["周一"],
    },
    "暑假": {
        "season_window_id": "WINDOW_SUMMER",
        "start_month": 7,
        "end_month": 8,
        "blocked_weekdays": ["周日"],
    },
    "秋季": {
        "season_window_id": "WINDOW_AUTUMN",
        "start_month": 9,
        "end_month": 12,
        "blocked_weekdays": ["周一"],
    },
}
SEASON_WINDOW_OPTIONS = tuple(
    {
        "season_window_id": SEASON_WINDOW_DEFAULTS[name]["season_window_id"],
        "name": name,
        "start_month": SEASON_WINDOW_DEFAULTS[name]["start_month"],
        "end_month": SEASON_WINDOW_DEFAULTS[name]["end_month"],
        "blocked_weekdays": list(SEASON_WINDOW_DEFAULTS[name]["blocked_weekdays"]),
    }
    for name in SEASON_WINDOW_ORDER
)
YEAR_SEASON_WINDOW_PATTERN = re.compile(r"^\d{4}\s*年?\s*[-_/]?\s*(寒假|春季|暑假|秋季)$")


def split_window_values(values: Any) -> list[str]:
    return split_delimited_values(values)


def season_window_tokens(value: Any) -> Set[str]:
    text = normalize_text(value)
    if not text:
        return set()

    tokens = {text}
    if text in SEASON_WINDOW_ID_TO_NAME:
        tokens.add(SEASON_WINDOW_ID_TO_NAME[text])
    if text in SEASON_WINDOW_NAME_TO_ID:
        tokens.add(SEASON_WINDOW_NAME_TO_ID[text])

    match = YEAR_SEASON_WINDOW_PATTERN.match(text)
    if match:
        season_name = match.group(1)
        tokens.add(season_name)
        tokens.add(SEASON_WINDOW_NAME_TO_ID[season_name])

    return tokens


def expanded_window_tokens(*values: Any) -> Set[str]:
    tokens: Set[str] = set()
    for value in values:
        for item in split_window_values(value):
            tokens.update(season_window_tokens(item))
    return tokens


def season_window_name_for_id(window_id: Any) -> str:
    return SEASON_WINDOW_ID_TO_NAME.get(normalize_text(window_id), "")


def season_window_id_for_name(name: Any) -> str:
    return SEASON_WINDOW_NAME_TO_ID.get(normalize_text(name), "")
