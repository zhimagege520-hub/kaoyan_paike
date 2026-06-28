from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple


def clean_cell(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_csv_with_fieldnames(path: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def read_csv_text_with_fieldnames(text: str) -> Tuple[List[str], List[Dict[str, str]]]:
    handle = io.StringIO(text.lstrip("\ufeff"), newline="")
    reader = csv.DictReader(handle)
    return list(reader.fieldnames or []), [dict(row) for row in reader]


def csv_rows_text(
    fieldnames: Sequence[str],
    rows: Iterable[dict],
    *,
    bom: bool = False,
    extrasaction: str = "ignore",
    value_formatter: Optional[Callable[[object], object]] = None,
) -> str:
    handle = io.StringIO(newline="")
    writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction=extrasaction)
    writer.writeheader()
    for row in rows:
        writer.writerow(format_csv_row(row, fieldnames, extrasaction, value_formatter))
    text = handle.getvalue()
    return f"\ufeff{text}" if bom else text


def format_csv_row(
    row: dict,
    fieldnames: Sequence[str],
    extrasaction: str,
    value_formatter: Optional[Callable[[object], object]],
) -> dict:
    if extrasaction == "raise":
        return {
            key: value_formatter(value) if value_formatter else value
            for key, value in row.items()
        }
    return {
        field: value_formatter(row.get(field, "")) if value_formatter else row.get(field, "")
        for field in fieldnames
    }


def write_csv_rows(
    path: Path,
    fieldnames: Sequence[str],
    rows: Iterable[dict],
    *,
    encoding: str = "utf-8-sig",
    extrasaction: str = "ignore",
    value_formatter: Optional[Callable[[object], object]] = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding=encoding) as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction=extrasaction)
        writer.writeheader()
        for row in rows:
            writer.writerow(format_csv_row(row, fieldnames, extrasaction, value_formatter))
