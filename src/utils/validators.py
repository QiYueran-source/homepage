"""数据验证器"""

from datetime import datetime
from typing import List, Dict, Any


def validate_date_format(date_str: str, format_str: str = "%Y.%m.%d") -> bool:
    """验证日期格式"""
    try:
        datetime.strptime(date_str, format_str)
        return True
    except (ValueError, TypeError):
        return False


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
    """验证必需字段，返回缺失的字段列表"""
    missing = []
    for field in required_fields:
        if not data.get(field):
            missing.append(field)
    return missing
