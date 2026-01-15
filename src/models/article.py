"""文章数据模型"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Article:
    """文章数据模型"""
    
    title: str
    date: str
    category: str
    slug: str
    content: str
    excerpt: str = ""
    image: str = ""
    file_path: str = ""
    tags: List[str] = field(default_factory=list)
    url: str = ""
    category_name: str = ""
    
    def __post_init__(self):
        """初始化后处理"""
        if not self.url:
            self.url = f"/blog/{self.slug}.html"
        
        if not self.category_name:
            self.category_name = self.category
