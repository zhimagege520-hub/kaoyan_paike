from __future__ import annotations

from typing import Any

from scripts.field_utils import normalize_text


PUBLIC_SUBJECTS_WITH_CHINESE = frozenset({"英语", "政治", "数学", "语文"})
PUBLIC_SUBJECT_SORT_ORDER = {"数学": 0, "英语": 1, "政治": 2, "语文": 3}
CORE_PUBLIC_SUBJECT_PREFERRED_PERIODS = {"数学": "AM", "英语": "PM", "政治": "PM"}


def subject_sort_value(subject: Any, default: int = 99) -> int:
    return PUBLIC_SUBJECT_SORT_ORDER.get(normalize_text(subject), default)
