from __future__ import annotations

from typing import Dict, Iterable, Tuple


TEMPLATE_SHEETS: Dict[str, str] = {
    "01_年度排课窗口表": "schedule_windows",
    "02_课节表": "time_slots",
    "03_教学区表": "teaching_areas",
    "04_教室表": "rooms",
    "05_教师基础信息表": "teachers",
    "06_教师不可排日期时段表": "teacher_unavailability",
    "07_产品管理表": "products",
    "08_产品课程课时表": "product_courses",
    "09_产品窗口排课规则表": "product_schedule_rules",
    "10_班级基础信息表": "classes",
    "11_班级排课窗口表": "class_window_boundaries",
    "12_班级老师安排表": "class_teacher_assignments",
    "13_班级排课互斥关系表": "class_conflict_groups",
    "14_锁定课表": "locked_scheduled_lessons",
    "15_教学区通勤关系表": "teaching_area_links",
    "16_全局停课日期表": "global_blackout_dates",
    "17_历史已排课明细表": "historical_scheduled_lessons",
    "18_ERP产品对应表": "business_product_mappings",
    "19_ERP标准产品清单": "erp_standard_products",
}

TEMPLATE_SHEET_ALIASES: Dict[str, Tuple[str, ...]] = {
    "11_班级排课窗口表": ("11_班级窗口边界表",),
    "18_ERP产品对应表": ("18_业务产品映射表",),
}


def template_sheet_table_pairs(include_aliases: bool = True) -> Iterable[Tuple[str, str]]:
    for sheet_name, table_name in TEMPLATE_SHEETS.items():
        yield sheet_name, table_name
        if include_aliases:
            for alias in TEMPLATE_SHEET_ALIASES.get(sheet_name, ()):
                yield alias, table_name
