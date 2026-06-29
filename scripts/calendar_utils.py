from __future__ import annotations

from datetime import date as Date, timedelta
from typing import Iterable, Set, Tuple


def parse_iso_date(value: Date | str) -> Date:
    return value if isinstance(value, Date) else Date.fromisoformat(value)


def iter_date_values(start: Date | str, end: Date | str) -> Iterable[str]:
    current = parse_iso_date(start)
    last = parse_iso_date(end)
    while current <= last:
        yield current.isoformat()
        current += timedelta(days=1)


def date_range(start: Date | str, end: Date | str) -> list[str]:
    return list(iter_date_values(start, end))


def date_range_values(start: Date | str, end: Date | str) -> Set[str]:
    return set(iter_date_values(start, end))


def week_start_date(value: Date | str) -> Date:
    day = parse_iso_date(value)
    return day - timedelta(days=day.weekday())


def week_start(value: Date | str) -> str:
    return week_start_date(value).isoformat()


def week_dates(week: Date | str) -> list[str]:
    start = parse_iso_date(week)
    return [(start + timedelta(days=offset)).isoformat() for offset in range(7)]


def iter_week_start_dates(start: Date | str, end: Date | str) -> Iterable[Date]:
    current = week_start_date(start)
    last = week_start_date(end)
    while current <= last:
        yield current
        current += timedelta(days=7)


def week_range(start: Date | str, end: Date | str) -> list[str]:
    return [week.isoformat() for week in iter_week_start_dates(start, end)]


def iso_week_key(value: Date | str) -> Tuple[int, int]:
    iso = parse_iso_date(value).isocalendar()
    return iso.year, iso.week


def week_start_from_iso_key(key: Tuple[int, int]) -> Date:
    return Date.fromisocalendar(key[0], key[1], 1)


def week_display_label(monday: Date | str) -> str:
    value = parse_iso_date(monday)
    iso = value.isocalendar()
    return f"{iso.year}年第{iso.week}周({value.isoformat()}起)"
