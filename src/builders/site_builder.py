"""网站构建器（主构建器）"""

from pathlib import Path
from typing import List

from src.config import Config
from src.loaders.yaml_loader import YAMLLoader
from src.loaders.blog_loader import BlogLoader
from src.processors.category_mapper import CategoryMapper
from src.builders.page_builder import PageBuilder
from src.builders.article_builder import ArticleBuilder
from src.models.site_data import SiteData
from src.models.article import Article
from src.utils.file_utils import ensure_dir, copy_static_files
from src.utils.exceptions import BuilderError


class SiteBuilder:
    """网站构建器"""
    
    def __init__(self, config: Config):
        """
        初始化网站构建器
        
        Args:
            config: 配置对象
        """
        self.config = config
        self.yaml_loader = YAMLLoader(config.encoding)
        self.page_builder = PageBuilder(config.templates_dir, config.encoding)
        self.article_builder = ArticleBuilder(config.templates_dir, config.encoding)
        
        # 加载分类映射
        category_mapper = CategoryMapper(config.category_mapping_file)
        self.category_mapper = category_mapper
    
    def build(self) -> None:
        """构建整个网站"""
        print("开始构建网站...")
        
        # 创建输出目录
        ensure_dir(self.config.dist_dir)
        
        # 加载数据
        site_data = self._load_site_data()
        
        # 构建页面
        self._build_pages(site_data)
        
        # 构建文章
        self._build_articles(site_data)
        
        # 复制静态文件
        self._copy_static_files()
        
        print("网站构建完成！")
    
    def _load_site_data(self) -> SiteData:
        """加载网站数据"""
        print("加载数据文件...")
        
        data_dir = self.config.data_dir
        
        # 加载YAML数据
        personal = self.yaml_loader.load(data_dir / "personal.yaml")
        education = self.yaml_loader.load_safe(data_dir / "education.yaml", {})
        experience = self.yaml_loader.load_safe(data_dir / "experience.yaml", {})
        projects = self.yaml_loader.load_safe(data_dir / "projects.yaml", {})
        tech_stack = self.yaml_loader.load_safe(data_dir / "tech-stack.yaml", {})
        honors = self.yaml_loader.load_safe(data_dir / "documents" / "honors.yaml", {})
        certificates = self.yaml_loader.load_safe(data_dir / "documents" / "certificates.yaml", {})
        factor_docs = self.yaml_loader.load_safe(data_dir / "documents" / "factor-docs.yaml", {})
        datasets = self.yaml_loader.load_safe(data_dir / "documents" / "datasets.yaml", {})
        
        # 加载博客文章
        print("加载博客文章...")
        blog_dir = data_dir / "blog"
        blog_loader = BlogLoader(blog_dir, self.config.encoding)
        
        categories = blog_loader.get_categories()
        articles_by_category = blog_loader.load_all_articles()
        
        # 合并所有文章
        all_articles: List[Article] = []
        for category_articles in articles_by_category.values():
            all_articles.extend(category_articles)
        
        # 按日期排序
        all_articles.sort(key=lambda x: x.date, reverse=True)
        
        # 应用分类映射
        category_name_mapping = self.category_mapper.get_all_categories()
        for article in all_articles:
            article.category_name = self.category_mapper.get_name(article.category)
        
        # 打印加载信息
        for category, articles in articles_by_category.items():
            if articles:
                print(f"  - {category}: {len(articles)} 篇文章")
        
        # 创建SiteData对象
        site_data = SiteData(
            personal=personal,
            education=education.get('education', []),
            experiences=experience.get('experiences', []),
            projects=projects.get('projects', []),
            tech_stack=tech_stack.get('tech_stack', []),
            honors=honors.get('honors', []),
            certificates=certificates.get('certificates', []),
            factor_docs=factor_docs.get('factor_docs', []),
            datasets=datasets.get('datasets', []),
            articles=all_articles,
            articles_by_category={
                cat: articles for cat, articles in articles_by_category.items()
            },
            categories=categories,
            category_name_mapping=category_name_mapping
        )
        
        return site_data
    
    def _build_pages(self, site_data: SiteData) -> None:
        """构建页面"""
        print("渲染HTML模板...")
        
        context = site_data.to_dict()
        
        # 构建首页
        index_path = self.config.dist_dir / "index.html"
        self.page_builder.build('index.html', context, index_path)
        print(f"首页构建完成！输出文件: {index_path}")
        
        # 构建简历页
        resume_path = self.config.dist_dir / "resume.html"
        self.page_builder.build('resume.html', context, resume_path)
        print(f"简历页面构建完成！输出文件: {resume_path}")
    
    def _build_articles(self, site_data: SiteData) -> None:
        """构建文章详情页"""
        print("生成文章详情页...")
        
        blog_output_dir = self.config.dist_dir / "blog"
        ensure_dir(blog_output_dir)
        
        # 构建所有文章详情页
        self.article_builder.build_all(site_data.articles, site_data, blog_output_dir)
        
        for article in site_data.articles:
            print(f"  - {article.slug}.html")
        
        print(f"文章详情页构建完成！共 {len(site_data.articles)} 篇文章")
        
        # 构建文章索引
        index_path = blog_output_dir / "index.json"
        self.article_builder.build_index(site_data.articles, site_data.categories, index_path)
        print(f"文章索引已生成: {index_path}")
    
    def _copy_static_files(self) -> None:
        """复制静态文件"""
        if self.config.static_dir.exists():
            static_dest = self.config.dist_dir / "static"
            copy_static_files(self.config.static_dir, static_dest)
            print(f"静态文件已复制到: {static_dest}")
