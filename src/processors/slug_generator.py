"""Slug生成器"""

import re
from typing import Optional


def slugify(text: Optional[str]) -> str:
    """
    将文本转换为 URL 友好的 slug
    
    Args:
        text: 要转换的文本
        
    Returns:
        URL友好的slug字符串
    """
    if not text:
        return ""
    
    # 转换为小写
    text = str(text).lower()
    
    # 替换空格和特殊字符为连字符
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    
    # 移除首尾连字符
    text = text.strip('-')
    
    return text


def generate_slug_from_filename(filename: str) -> str:
    """
    从文件名生成slug（移除日期前缀）
    
    Args:
        filename: 文件名（不含扩展名）
        
    Returns:
        slug字符串
    """
    # 移除日期前缀（格式：2025-01-05-title）
    date_pattern = r'^\d{4}-\d{2}-\d{2}-'
    slug = re.sub(date_pattern, '', filename)
    
    return slug if slug else ""
