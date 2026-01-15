"""页面构建器基类"""

from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader

from src.utils.exceptions import BuilderError


class PageBuilder:
    """页面构建器基类"""
    
    def __init__(self, templates_dir: Path, encoding: str = "utf-8"):
        """
        初始化页面构建器
        
        Args:
            templates_dir: 模板目录
            encoding: 文件编码
        """
        self.templates_dir = templates_dir
        self.encoding = encoding
        self.env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=True
        )
    
    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        渲染模板
        
        Args:
            template_name: 模板文件名
            context: 模板上下文
            
        Returns:
            渲染后的HTML内容
            
        Raises:
            BuilderError: 渲染失败时抛出
        """
        try:
            template = self.env.get_template(template_name)
            return template.render(**context)
        except Exception as e:
            raise BuilderError(f"渲染模板失败 {template_name}: {e}")
    
    def build(self, template_name: str, context: Dict[str, Any], output_path: Path) -> None:
        """
        构建页面并写入文件
        
        Args:
            template_name: 模板文件名
            context: 模板上下文
            output_path: 输出文件路径
            
        Raises:
            BuilderError: 构建失败时抛出
        """
        try:
            html_content = self.render(template_name, context)
            
            # 确保输出目录存在
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 写入文件
            with open(output_path, 'w', encoding=self.encoding) as f:
                f.write(html_content)
        except Exception as e:
            raise BuilderError(f"构建页面失败 {output_path}: {e}")
