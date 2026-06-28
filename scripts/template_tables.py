from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Iterable, Mapping, Optional, Sequence, Tuple


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

BUSINESS_SOURCE_TABLES: Tuple[str, ...] = (
    "business_classes",
    "scheduled_lessons",
)

BASE_TABLE_ALIASES: Dict[str, str] = {
    "schedulewindows": "schedule_windows",
    "schedulewindow": "schedule_windows",
    "年度排课窗口": "schedule_windows",
    "年度排课窗口表": "schedule_windows",
    "排课窗口": "schedule_windows",
    "排课窗口表": "schedule_windows",
    "timeslots": "time_slots",
    "timeslot": "time_slots",
    "time_slots": "time_slots",
    "课节": "time_slots",
    "课节表": "time_slots",
    "teachingareas": "teaching_areas",
    "teachingarea": "teaching_areas",
    "教学区": "teaching_areas",
    "教学区表": "teaching_areas",
    "rooms": "rooms",
    "room": "rooms",
    "教室": "rooms",
    "教室表": "rooms",
    "教学区与教室": "rooms",
    "teachers": "teachers",
    "teacher": "teachers",
    "教师": "teachers",
    "教师表": "teachers",
    "教师基础信息": "teachers",
    "教师基础信息表": "teachers",
    "teacherunavailability": "teacher_unavailability",
    "teacherunavailable": "teacher_unavailability",
    "教师不可排日期时段": "teacher_unavailability",
    "教师不可排日期时段表": "teacher_unavailability",
    "教师不可排时间": "teacher_unavailability",
    "教师不可排时间表": "teacher_unavailability",
    "products": "products",
    "product": "products",
    "产品": "products",
    "产品表": "products",
    "产品管理": "products",
    "产品管理表": "products",
    "productcourses": "product_courses",
    "courses": "product_courses",
    "productrequirements": "product_courses",
    "产品课程": "product_courses",
    "产品课程表": "product_courses",
    "产品课程课时": "product_courses",
    "产品课程课时表": "product_courses",
    "productschedulerules": "product_schedule_rules",
    "schedulerules": "product_schedule_rules",
    "productrules": "product_schedule_rules",
    "产品排课规则": "product_schedule_rules",
    "产品排课规则表": "product_schedule_rules",
    "产品窗口排课规则": "product_schedule_rules",
    "产品窗口排课规则表": "product_schedule_rules",
    "classes": "classes",
    "class": "classes",
    "班级": "classes",
    "班级表": "classes",
    "班级管理": "classes",
    "班级基础信息": "classes",
    "班级基础信息表": "classes",
    "classwindowboundaries": "class_window_boundaries",
    "classwindowboundary": "class_window_boundaries",
    "班级窗口边界": "class_window_boundaries",
    "班级窗口边界表": "class_window_boundaries",
    "班级排课窗口": "class_window_boundaries",
    "班级排课窗口表": "class_window_boundaries",
    "classteacherassignments": "class_teacher_assignments",
    "teacherassignments": "class_teacher_assignments",
    "classteachers": "class_teacher_assignments",
    "班级老师安排": "class_teacher_assignments",
    "班级老师安排表": "class_teacher_assignments",
    "classconflictgroups": "class_conflict_groups",
    "conflictgroups": "class_conflict_groups",
    "班级互斥关系": "class_conflict_groups",
    "班级互斥关系表": "class_conflict_groups",
    "班级排课互斥关系": "class_conflict_groups",
    "班级排课互斥关系表": "class_conflict_groups",
    "排课互斥关系": "class_conflict_groups",
    "冲突组": "class_conflict_groups",
    "冲突组表": "class_conflict_groups",
    "teachingarealinks": "teaching_area_links",
    "arealinks": "teaching_area_links",
    "教学区关联": "teaching_area_links",
    "教学区关联表": "teaching_area_links",
    "教学区通勤关系": "teaching_area_links",
    "教学区通勤关系表": "teaching_area_links",
    "globalblackoutdates": "global_blackout_dates",
    "blackoutdates": "global_blackout_dates",
    "blackouts": "global_blackout_dates",
    "全局停课日期": "global_blackout_dates",
    "全局停课日期表": "global_blackout_dates",
    "停课日期": "global_blackout_dates",
    "历史已排课明细": "historical_scheduled_lessons",
    "历史已排课明细表": "historical_scheduled_lessons",
    "erp产品对应": "business_product_mappings",
    "erp产品对应表": "business_product_mappings",
    "businessproductmappings": "business_product_mappings",
    "businessproductmapping": "business_product_mappings",
    "业务产品对应": "business_product_mappings",
    "业务产品对应表": "business_product_mappings",
    "erpstandardproducts": "erp_standard_products",
    "erpstandardproduct": "erp_standard_products",
    "erp标准产品": "erp_standard_products",
    "erp标准产品清单": "erp_standard_products",
    "erp标准产品清单表": "erp_standard_products",
    "businessclasses": "business_classes",
    "businessclassexport": "business_classes",
    "businessclassrows": "business_classes",
    "业务班级": "business_classes",
    "业务班级导出": "business_classes",
    "班级查询导出": "business_classes",
    "businessproductmap": "business_product_mappings",
    "productmap": "business_product_mappings",
    "业务产品映射": "business_product_mappings",
    "业务产品映射表": "business_product_mappings",
    "产品映射": "business_product_mappings",
    "产品映射表": "business_product_mappings",
    "scheduledlessons": "scheduled_lessons",
    "scheduledlesson": "scheduled_lessons",
    "schedulehistory": "scheduled_lessons",
    "historicalschedule": "scheduled_lessons",
    "已排课明细": "scheduled_lessons",
    "历史课表": "scheduled_lessons",
    "已排课表": "scheduled_lessons",
    "已排课": "scheduled_lessons",
    "locked_scheduled_lessons": "locked_scheduled_lessons",
    "lockedlessons": "locked_scheduled_lessons",
    "lockedschedule": "locked_scheduled_lessons",
    "锁定课表": "locked_scheduled_lessons",
    "锁定课表表": "locked_scheduled_lessons",
    "已定课表": "locked_scheduled_lessons",
    "固定课表": "locked_scheduled_lessons",
}


def template_sheet_table_pairs(include_aliases: bool = True) -> Iterable[Tuple[str, str]]:
    for sheet_name, table_name in TEMPLATE_SHEETS.items():
        yield sheet_name, table_name
        if include_aliases:
            for alias in TEMPLATE_SHEET_ALIASES.get(sheet_name, ()):
                yield alias, table_name


def normalize_table_name(value: str) -> str:
    text = Path(value).stem if "." in value else value
    return (
        text.strip()
        .lower()
        .replace(" ", "")
        .replace("_", "")
        .replace("-", "")
        .replace("/", "")
        .replace("\\", "")
        .replace("（", "")
        .replace("）", "")
        .replace("(", "")
        .replace(")", "")
    )


def build_table_aliases(source_table_names: Sequence[str]) -> Dict[str, str]:
    aliases = dict(BASE_TABLE_ALIASES)
    for source_table_name in source_table_names:
        aliases.setdefault(normalize_table_name(source_table_name), source_table_name)
    for sheet_name, table_name in template_sheet_table_pairs():
        aliases.setdefault(normalize_table_name(sheet_name), table_name)
    return aliases


def table_name_for(value: str, aliases: Mapping[str, str]) -> Optional[str]:
    normalized = normalize_table_name(value)
    candidates = [normalized]
    unnumbered = re.sub(r"^\d+", "", normalized)
    if unnumbered and unnumbered != normalized:
        candidates.append(unnumbered)
    if "班级查询导出" in normalized:
        return "business_classes"
    if "配课明细" in normalized:
        return "scheduled_lessons"
    for candidate in candidates:
        table_name = aliases.get(candidate)
        if table_name:
            return table_name
    return None
