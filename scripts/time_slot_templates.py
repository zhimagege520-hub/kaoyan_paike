from __future__ import annotations

from typing import Any


DEFAULT_LESSON_TEMPLATES = (
    {
        "period": "AM",
        "suffix": "1",
        "name": "上午一",
        "order": 1,
        "start_time": "08:00",
        "end_time": "10:00",
        "duration_hours": 2,
    },
    {
        "period": "AM",
        "suffix": "2",
        "name": "上午二",
        "order": 2,
        "start_time": "10:20",
        "end_time": "12:20",
        "duration_hours": 2,
    },
    {
        "period": "PM",
        "suffix": "1",
        "name": "下午一",
        "order": 1,
        "start_time": "14:00",
        "end_time": "16:00",
        "duration_hours": 2,
    },
    {
        "period": "PM",
        "suffix": "2",
        "name": "下午二",
        "order": 2,
        "start_time": "16:20",
        "end_time": "18:20",
        "duration_hours": 2,
    },
    {
        "period": "EVENING",
        "suffix": "1",
        "name": "晚上",
        "order": 1,
        "start_time": "19:00",
        "end_time": "21:00",
        "duration_hours": 2,
    },
)


def default_lesson_template_rows() -> list[dict[str, Any]]:
    return [dict(template) for template in DEFAULT_LESSON_TEMPLATES]
