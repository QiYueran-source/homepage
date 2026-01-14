#!/usr/bin/env python3
"""
静态网站构建脚本
从YAML和Markdown文件生成HTML
"""

import os
import yaml
import markdown
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import frontmatter

# 配置路径
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"
DIST_DIR = BASE_DIR / "dist"
STATIC_DIR = BASE_DIR / "static"

def load_yaml(file_path):
    """加载YAML文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_markdown_files(directory):
    """加载目录下的所有Markdown文件"""
    articles = []
    md_files = sorted(Path(directory).glob("*.md"), reverse=True)
    
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            
            article = {
                'title': post.metadata.get('title', ''),
                'date': post.metadata.get('date', ''),
                'category': post.metadata.get('category', ''),
                'image': post.metadata.get('image', ''),
                'excerpt': post.metadata.get('excerpt', ''),
                'content': markdown.markdown(post.content)
            }
            articles.append(article)
    
    return articles

def build_site():
    """构建网站"""
    print("开始构建网站...")
    
    # 创建输出目录
    DIST_DIR.mkdir(exist_ok=True)
    
    # 加载数据
    print("加载数据文件...")
    personal = load_yaml(DATA_DIR / "personal.yaml")
    education = load_yaml(DATA_DIR / "education.yaml")
    experience = load_yaml(DATA_DIR / "experience.yaml")
    projects = load_yaml(DATA_DIR / "projects.yaml")
    tech_stack = load_yaml(DATA_DIR / "tech-stack.yaml")
    honors = load_yaml(DATA_DIR / "documents" / "honors.yaml")
    certificates = load_yaml(DATA_DIR / "documents" / "certificates.yaml")
    factor_docs = load_yaml(DATA_DIR / "documents" / "factor-docs.yaml")
    datasets = load_yaml(DATA_DIR / "documents" / "datasets.yaml")
    
    # 加载博客文章
    print("加载博客文章...")
    tech_notes = load_markdown_files(DATA_DIR / "blog" / "tech-notes")
    finance = load_markdown_files(DATA_DIR / "blog" / "finance")
    essays = load_markdown_files(DATA_DIR / "blog" / "essays")
    
    # 合并所有文章并按日期排序
    all_articles = tech_notes + finance + essays
    all_articles.sort(key=lambda x: x['date'], reverse=True)
    
    # 准备模板上下文
    context = {
        'personal': personal,
        'education': education.get('education', []),
        'experiences': experience.get('experiences', []),
        'projects': projects.get('projects', []),
        'tech_stack': tech_stack.get('tech_stack', []),
        'honors': honors.get('honors', []),
        'certificates': certificates.get('certificates', []),
        'factor_docs': factor_docs.get('factor_docs', []),
        'datasets': datasets.get('datasets', []),
        'articles': all_articles,
        'tech_notes': tech_notes,
        'finance': finance,
        'essays': essays
    }
    
    # 设置Jinja2环境
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=True
    )
    
    # 渲染主页面
    print("渲染HTML模板...")
    template = env.get_template('index.html')
    html_content = template.render(**context)
    
    # 写入输出文件
    output_file = DIST_DIR / "index.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"构建完成！输出文件: {output_file}")
    
    # 复制静态文件（如果存在）
    if STATIC_DIR.exists():
        import shutil
        static_dest = DIST_DIR / "static"
        if static_dest.exists():
            shutil.rmtree(static_dest)
        shutil.copytree(STATIC_DIR, static_dest)
        print(f"静态文件已复制到: {static_dest}")

if __name__ == "__main__":
    build_site()

