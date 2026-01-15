"""博客文章加载器"""

from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict

from src.loaders.markdown_loader import MarkdownLoader
from src.processors.slug_generator import slugify, generate_slug_from_filename
from src.models.article import Article
from src.utils.exceptions import LoaderError


class BlogLoader:
    """博客文章加载器"""
    
    def __init__(self, blog_dir: Path, encoding: str = "utf-8"):
        """
        初始化博客加载器
        
        Args:
            blog_dir: 博客目录路径
            encoding: 文件编码
        """
        self.blog_dir = blog_dir
        self.markdown_loader = MarkdownLoader(encoding)
    
    def get_categories(self) -> List[str]:
        """
        获取所有分类目录
        
        Returns:
            分类名称列表
        """
        if not self.blog_dir.exists():
            return []
        
        categories = [
            d.name for d in self.blog_dir.iterdir()
            if d.is_dir() and not d.name.startswith('.')
        ]
        
        return sorted(categories)
    
    def load_articles_from_category(self, category: str) -> List[Article]:
        """
        从指定分类加载文章
        
        Args:
            category: 分类名称
            
        Returns:
            文章列表
        """
        category_dir = self.blog_dir / category
        if not category_dir.exists():
            return []
        
        articles = []
        md_files = sorted(category_dir.glob("*.md"), reverse=True)
        
        for md_file in md_files:
            try:
                article = self._load_article(md_file, category)
                articles.append(article)
            except LoaderError as e:
                print(f"警告: 跳过文章 {md_file}: {e}")
                continue
        
        return articles
    
    def load_all_articles(self) -> Dict[str, List[Article]]:
        """
        加载所有分类的文章
        
        Returns:
            按分类组织的文章字典
        """
        categories = self.get_categories()
        articles_by_category = {}
        
        for category in categories:
            articles = self.load_articles_from_category(category)
            articles_by_category[category] = articles
        
        return articles_by_category
    
    def _load_article(self, md_file: Path, category: str) -> Article:
        """
        加载单篇文章
        
        Args:
            md_file: Markdown文件路径
            category: 分类名称
            
        Returns:
            Article对象
        """
        data = self.markdown_loader.load(md_file)
        metadata = data['metadata']
        content = data['content_html']
        
        # 生成slug
        filename_slug = generate_slug_from_filename(md_file.stem)
        if not filename_slug:
            title = metadata.get('title', '')
            filename_slug = slugify(title) if title else "untitled"
        
        # 获取分类（优先使用metadata）
        article_category = metadata.get('category', category)
        
        # 获取相对路径
        file_path = str(md_file.relative_to(self.blog_dir))
        
        # 创建Article对象
        article = Article(
            title=metadata.get('title', 'Untitled'),
            date=metadata.get('date', ''),
            category=article_category,
            slug=filename_slug,
            content=content,
            excerpt=metadata.get('excerpt', ''),
            image=metadata.get('image', ''),
            file_path=file_path,
            tags=metadata.get('tags', [])
        )
        
        return article
