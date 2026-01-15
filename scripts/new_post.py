#!/usr/bin/env python3
"""
文章创建脚手架脚本
交互式创建新博客文章
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import Config
from src.processors.slug_generator import slugify
from src.utils.file_utils import ensure_dir
from src.utils.exceptions import SiteBuilderError


def get_existing_categories(blog_dir: Path) -> list:
    """获取现有的分类目录"""
    if not blog_dir.exists():
        return []
    categories = [d.name for d in blog_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    return sorted(categories)


def generate_filename(title: str, date_str: str) -> str:
    """生成文件名"""
    date_part = date_str.replace('.', '-')
    title_slug = slugify(title)
    if not title_slug:
        title_slug = "new-post"
    filename = f"{date_part}-{title_slug}.md"
    return filename


def create_post(title: str, category: str, date_str: str, excerpt: str = "", image: str = "", blog_dir: Path = None):
    """创建新文章文件"""
    if blog_dir is None:
        config = Config()
        blog_dir = config.data_dir / "blog"
    
    # 创建分类目录
    category_dir = blog_dir / category
    ensure_dir(category_dir)
    
    # 生成文件名
    filename = generate_filename(title, date_str)
    filepath = category_dir / filename
    
    # 检查文件是否已存在
    if filepath.exists():
        print(f"⚠️  警告：文件已存在：{filepath}")
        response = input("是否覆盖？(y/N): ").strip().lower()
        if response != 'y':
            print("❌ 已取消")
            return None
    
    # 生成 frontmatter
    frontmatter = f"""---
title: "{title}"
date: "{date_str}"
category: "{category}"
image: "{image if image else 'https://picsum.photos/seed/' + slugify(title) + '/800/500'}"
excerpt: "{excerpt}"
tags: []
---

# {title}

在这里开始写你的文章内容...

"""
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
    
    print(f"✅ 文章已创建：{filepath}")
    return filepath


def main():
    """主函数：交互式创建文章"""
    print("=" * 50)
    print("📝 创建新博客文章")
    print("=" * 50)
    
    try:
        config = Config()
        blog_dir = config.data_dir / "blog"
        
        # 获取现有分类
        existing_categories = get_existing_categories(blog_dir)
        
        # 输入标题
        title = input("\n📌 文章标题: ").strip()
        if not title:
            print("❌ 标题不能为空")
            sys.exit(1)
        
        # 输入分类
        if existing_categories:
            print(f"\n📁 现有分类: {', '.join(existing_categories)}")
            category = input("📁 分类（输入新分类名称或选择现有分类）: ").strip()
        else:
            category = input("📁 分类名称: ").strip()
        
        if not category:
            print("❌ 分类不能为空")
            sys.exit(1)
        
        # 输入日期
        today = datetime.now().strftime("%Y.%m.%d")
        date_input = input(f"📅 发布日期 (默认: {today}): ").strip()
        date_str = date_input if date_input else today
        
        # 验证日期格式
        try:
            datetime.strptime(date_str, "%Y.%m.%d")
        except ValueError:
            print("❌ 日期格式错误，应为 YYYY.MM.DD")
            sys.exit(1)
        
        # 输入摘要
        excerpt = input("📄 文章摘要（可选）: ").strip()
        
        # 输入图片 URL
        image = input("🖼️  封面图片 URL（可选，留空使用默认）: ").strip()
        
        # 创建文章
        filepath = create_post(title, category, date_str, excerpt, image, blog_dir)
        
        if filepath:
            print("\n" + "=" * 50)
            print("✨ 文章创建成功！")
            print(f"📂 文件位置: {filepath}")
            print("\n💡 提示：")
            print("   1. 编辑文章内容")
            print("   2. 运行 python build.py 构建网站")
            print("   3. 访问 http://localhost:8000/dist/index.html#blog 查看")
            print("=" * 50)
    
    except SiteBuilderError as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ 已取消")
        sys.exit(1)


if __name__ == "__main__":
    main()
