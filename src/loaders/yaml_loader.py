"""YAML文件加载器"""

from pathlib import Path
from typing import Any, Dict
import yaml

from src.utils.exceptions import LoaderError


class YAMLLoader:
    """YAML文件加载器"""
    
    def __init__(self, encoding: str = "utf-8"):
        """
        初始化YAML加载器
        
        Args:
            encoding: 文件编码
        """
        self.encoding = encoding
    
    def load(self, file_path: Path) -> Dict[str, Any]:
        """
        加载YAML文件
        
        Args:
            file_path: YAML文件路径
            
        Returns:
            解析后的字典
            
        Raises:
            LoaderError: 加载失败时抛出
        """
        if not file_path.exists():
            raise LoaderError(f"文件不存在: {file_path}")
        
        try:
            with open(file_path, 'r', encoding=self.encoding) as f:
                data = yaml.safe_load(f)
                return data if data is not None else {}
        except yaml.YAMLError as e:
            raise LoaderError(f"YAML解析错误 {file_path}: {e}")
        except Exception as e:
            raise LoaderError(f"读取文件失败 {file_path}: {e}")
    
    def load_safe(self, file_path: Path, default: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        安全加载YAML文件（失败时返回默认值）
        
        Args:
            file_path: YAML文件路径
            default: 默认值
            
        Returns:
            解析后的字典或默认值
        """
        if default is None:
            default = {}
        
        try:
            return self.load(file_path)
        except LoaderError:
            return default
