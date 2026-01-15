"""Markdown文件加载器"""

from pathlib import Path
from typing import Dict, Any
import markdown
import frontmatter

from src.utils.exceptions import LoaderError


class MarkdownLoader:
    """Markdown文件加载器"""
    
    def __init__(self, encoding: str = "utf-8"):
        """
        初始化Markdown加载器
        
        Args:
            encoding: 文件编码
        """
        self.encoding = encoding
    
    def load(self, file_path: Path) -> Dict[str, Any]:
        """
        加载Markdown文件（带frontmatter）
        
        Args:
            file_path: Markdown文件路径
            
        Returns:
            包含metadata和content的字典
            
        Raises:
            LoaderError: 加载失败时抛出
        """
        if not file_path.exists():
            raise LoaderError(f"文件不存在: {file_path}")
        
        try:
            with open(file_path, 'r', encoding=self.encoding) as f:
                post = frontmatter.load(f)
                
                return {
                    'metadata': post.metadata,
                    'content': post.content,
                    'content_html': markdown.markdown(post.content)
                }
        except Exception as e:
            raise LoaderError(f"加载Markdown文件失败 {file_path}: {e}")
