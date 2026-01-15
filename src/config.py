"""配置管理模块"""

from pathlib import Path
from typing import Dict, Any, Optional
import yaml
import os

from src.utils.exceptions import ConfigError


class Config:
    """配置管理器"""
    
    def __init__(self, config_file: Optional[Path] = None, base_dir: Optional[Path] = None):
        """
        初始化配置
        
        Args:
            config_file: 配置文件路径，默认为 config/settings.yaml
            base_dir: 项目根目录，默认为当前文件的父目录的父目录
        """
        if base_dir is None:
            base_dir = Path(__file__).parent.parent
        
        if config_file is None:
            config_file = base_dir / "config" / "settings.yaml"
        
        self.base_dir = base_dir
        self.config_file = config_file
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f) or {}
        except FileNotFoundError:
            raise ConfigError(f"配置文件不存在: {self.config_file}")
        except yaml.YAMLError as e:
            raise ConfigError(f"配置文件格式错误: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值（支持点号分隔的嵌套键）
        
        Args:
            key: 配置键，如 "paths.data" 或 "blog.categories_file"
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        # 支持环境变量覆盖
        env_key = key.upper().replace('.', '_')
        env_value = os.getenv(env_key)
        if env_value is not None:
            return env_value
        
        return value
    
    def get_path(self, key: str) -> Path:
        """
        获取路径配置（相对于base_dir）
        
        Args:
            key: 配置键，如 "paths.data"
            
        Returns:
            Path对象
        """
        path_str = self.get(key)
        if not path_str:
            raise ConfigError(f"路径配置不存在: {key}")
        
        if os.path.isabs(path_str):
            return Path(path_str)
        
        return self.base_dir / path_str
    
    @property
    def data_dir(self) -> Path:
        """数据目录"""
        return self.get_path("paths.data")
    
    @property
    def templates_dir(self) -> Path:
        """模板目录"""
        return self.get_path("paths.templates")
    
    @property
    def dist_dir(self) -> Path:
        """输出目录"""
        return self.get_path("paths.dist")
    
    @property
    def static_dir(self) -> Path:
        """静态文件目录"""
        return self.get_path("paths.static")
    
    @property
    def encoding(self) -> str:
        """文件编码"""
        return self.get("build.encoding", "utf-8")
    
    @property
    def category_mapping_file(self) -> Path:
        """分类映射文件路径"""
        mapping_file = self.get("blog.categories_file")
        if not mapping_file:
            raise ConfigError("分类映射文件配置不存在")
        
        if os.path.isabs(mapping_file):
            return Path(mapping_file)
        
        return self.base_dir / mapping_file
