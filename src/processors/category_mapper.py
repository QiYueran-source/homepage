"""分类映射处理器"""

from pathlib import Path
from typing import Dict, Optional
import yaml

from src.utils.exceptions import ConfigError


class CategoryMapper:
    """分类名称映射器"""
    
    def __init__(self, mapping_file: Path):
        """
        初始化分类映射器
        
        Args:
            mapping_file: 分类映射文件路径
        """
        self.mapping_file = mapping_file
        self._mapping: Dict[str, str] = {}
        self._load_mapping()
    
    def _load_mapping(self) -> None:
        """加载分类映射"""
        if not self.mapping_file.exists():
            raise ConfigError(f"分类映射文件不存在: {self.mapping_file}")
        
        try:
            with open(self.mapping_file, 'r', encoding='utf-8') as f:
                self._mapping = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ConfigError(f"分类映射文件格式错误: {e}")
    
    def get_name(self, category: str) -> str:
        """
        获取分类的中文名称
        
        Args:
            category: 分类标识（英文）
            
        Returns:
            分类的中文名称，如果不存在则返回原值
        """
        return self._mapping.get(category, category)
    
    def get_all_categories(self) -> Dict[str, str]:
        """获取所有分类映射"""
        return self._mapping.copy()
