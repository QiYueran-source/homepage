"""文章详情页构建器"""

from pathlib import Path
from typing import List, Optional
import json

from src.builders.page_builder import PageBuilder
from src.models.article import Article
from src.models.site_data import SiteData
from src.utils.exceptions import BuilderError


class ArticleBuilder(PageBuilder):
    """文章详情页构建器"""
    
    def build_all(self, articles: List[Article], site_data: SiteData, output_dir: Path) -> None:
        """
        构建所有文章详情页
        
        Args:
            articles: 文章列表
            site_data: 网站数据
            output_dir: 输出目录
        """
        context = site_data.to_dict()
        
        for i, article in enumerate(articles):
            # 获取上一篇和下一篇文章
            prev_article = articles[i - 1] if i > 0 else None
            next_article = articles[i + 1] if i < len(articles) - 1 else None
            
            # 准备文章上下文
            article_context = {
                **context,
                'article': site_data._article_to_dict(article),
                'prev_article': site_data._article_to_dict(prev_article) if prev_article else None,
                'next_article': site_data._article_to_dict(next_article) if next_article else None
            }
            
            # 构建文章页面
            output_path = output_dir / f"{article.slug}.html"
            self.build('article.html', article_context, output_path)
    
    def build_index(self, articles: List[Article], categories: List[str], output_path: Path) -> None:
        """
        构建文章索引JSON
        
        Args:
            articles: 文章列表
            categories: 分类列表
            output_path: 输出文件路径
        """
        articles_index = {
            'articles': [
                {
                    'title': a.title,
                    'date': a.date,
                    'category': a.category,
                    'slug': a.slug,
                    'url': a.url,
                    'excerpt': a.excerpt,
                    'image': a.image
                }
                for a in articles
            ],
            'categories': categories
        }
        
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(articles_index, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise BuilderError(f"构建文章索引失败 {output_path}: {e}")
