"""网站数据模型"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

from src.models.article import Article


@dataclass
class SiteData:
    """网站数据模型"""
    
    personal: Dict[str, Any]
    education: List[Dict[str, Any]] = field(default_factory=list)
    experiences: List[Dict[str, Any]] = field(default_factory=list)
    projects: List[Dict[str, Any]] = field(default_factory=list)
    tech_stack: List[Dict[str, Any]] = field(default_factory=list)
    honors: List[Dict[str, Any]] = field(default_factory=list)
    certificates: List[Dict[str, Any]] = field(default_factory=list)
    factor_docs: List[Dict[str, Any]] = field(default_factory=list)
    datasets: List[Dict[str, Any]] = field(default_factory=list)
    articles: List[Article] = field(default_factory=list)
    articles_by_category: Dict[str, List[Article]] = field(default_factory=dict)
    categories: List[str] = field(default_factory=list)
    category_name_mapping: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（用于模板渲染）"""
        return {
            'personal': self.personal,
            'education': self.education,
            'experiences': self.experiences,
            'projects': self.projects,
            'tech_stack': self.tech_stack,
            'honors': self.honors,
            'certificates': self.certificates,
            'factor_docs': self.factor_docs,
            'datasets': self.datasets,
            'articles': [self._article_to_dict(a) for a in self.articles],
            'articles_by_category': {
                cat: [self._article_to_dict(a) for a in articles]
                for cat, articles in self.articles_by_category.items()
            },
            'categories': self.categories,
            'category_name_mapping': self.category_name_mapping
        }
    
    @staticmethod
    def _article_to_dict(article: Article) -> Dict[str, Any]:
        """将Article对象转换为字典"""
        return {
            'title': article.title,
            'date': article.date,
            'category': article.category,
            'slug': article.slug,
            'content': article.content,
            'excerpt': article.excerpt,
            'image': article.image,
            'file_path': article.file_path,
            'tags': article.tags,
            'url': article.url,
            'category_name': article.category_name
        }
