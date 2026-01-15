#!/usr/bin/env python3
"""
文章管理工具
列出、删除、编辑博客文章
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import Config
from src.loaders.blog_loader import BlogLoader
from src.utils.validators import validate_date_format, validate_required_fields
from src.utils.exceptions import SiteBuilderError


def get_all_articles(config: Config):
    """获取所有文章"""
    blog_dir = config.data_dir / "blog"
    blog_loader = BlogLoader(blog_dir, config.encoding)
    
    articles_by_category = blog_loader.load_all_articles()
    
    all_articles = []
    for category, articles in articles_by_category.items():
        for article in articles:
            all_articles.append({
                'file': blog_dir / article.file_path,
                'category': article.category,
                'title': article.title,
                'date': article.date,
                'excerpt': article.excerpt[:50] + '...' if article.excerpt else ''
            })
    
    # 按日期排序
    all_articles.sort(key=lambda x: x['date'], reverse=True)
    return all_articles


def list_articles(config: Config):
    """列出所有文章"""
    articles = get_all_articles(config)
    
    if not articles:
        print("📝 暂无文章")
        return
    
    print("=" * 80)
    print(f"📚 共 {len(articles)} 篇文章")
    print("=" * 80)
    
    for i, article in enumerate(articles, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   分类: {article['category']}")
        print(f"   日期: {article['date']}")
        print(f"   摘要: {article['excerpt']}")
        print(f"   路径: {article['file']}")


def delete_article(config: Config):
    """删除文章"""
    articles = get_all_articles(config)
    
    if not articles:
        print("📝 暂无文章可删除")
        return
    
    list_articles(config)
    
    try:
        index = int(input(f"\n选择要删除的文章编号 (1-{len(articles)}): ").strip())
        if index < 1 or index > len(articles):
            print("❌ 无效的编号")
            return
        
        article = articles[index - 1]
        print(f"\n⚠️  即将删除: {article['title']}")
        print(f"   路径: {article['file']}")
        
        confirm = input("确认删除？(y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ 已取消")
            return
        
        article['file'].unlink()
        print(f"✅ 已删除: {article['file']}")
        
    except ValueError:
        print("❌ 请输入有效的数字")
    except Exception as e:
        print(f"❌ 删除失败: {e}")


def validate_article(file_path: Path, config: Config):
    """验证文章格式"""
    from src.loaders.markdown_loader import MarkdownLoader
    
    loader = MarkdownLoader(config.encoding)
    
    try:
        data = loader.load(file_path)
        metadata = data['metadata']
        
        errors = []
        warnings = []
        
        # 检查必需的元数据
        required_fields = ['title', 'date', 'category']
        missing = validate_required_fields(metadata, required_fields)
        if missing:
            errors.extend([f"缺少必需字段: {field}" for field in missing])
        
        # 检查日期格式
        date = metadata.get('date', '')
        if date and not validate_date_format(date):
            errors.append(f"日期格式错误: {date} (应为 YYYY.MM.DD)")
        
        # 检查内容
        if not data['content'].strip():
            warnings.append("文章内容为空")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    except Exception as e:
        return {
            'valid': False,
            'errors': [f"读取文件失败: {e}"],
            'warnings': []
        }


def validate_all_articles(config: Config):
    """验证所有文章"""
    articles = get_all_articles(config)
    
    if not articles:
        print("📝 暂无文章")
        return
    
    print("=" * 80)
    print("🔍 验证所有文章")
    print("=" * 80)
    
    valid_count = 0
    invalid_count = 0
    
    for article in articles:
        result = validate_article(article['file'], config)
        
        if result['valid']:
            valid_count += 1
            status = "✅"
        else:
            invalid_count += 1
            status = "❌"
        
        print(f"\n{status} {article['title']}")
        print(f"   路径: {article['file']}")
        
        if result['errors']:
            for error in result['errors']:
                print(f"   ❌ {error}")
        
        if result['warnings']:
            for warning in result['warnings']:
                print(f"   ⚠️  {warning}")
    
    print("\n" + "=" * 80)
    print(f"✅ 有效: {valid_count} 篇")
    print(f"❌ 无效: {invalid_count} 篇")
    print("=" * 80)


def show_statistics(config: Config):
    """显示统计信息"""
    articles = get_all_articles(config)
    
    if not articles:
        print("📝 暂无文章")
        return
    
    # 按分类统计
    category_count = {}
    for article in articles:
        category = article['category']
        category_count[category] = category_count.get(category, 0) + 1
    
    print("=" * 80)
    print("📊 文章统计")
    print("=" * 80)
    print(f"\n总文章数: {len(articles)}")
    print("\n按分类统计:")
    for category, count in sorted(category_count.items()):
        print(f"  - {category}: {count} 篇")
    
    # 日期范围
    dates = [a['date'] for a in articles if a['date']]
    if dates:
        print(f"\n日期范围: {min(dates)} ~ {max(dates)}")


def main():
    """主函数"""
    try:
        config = Config()
        
        if len(sys.argv) > 1:
            command = sys.argv[1]
        else:
            print("=" * 50)
            print("📝 文章管理工具")
            print("=" * 50)
            print("\n可用命令:")
            print("  list       - 列出所有文章")
            print("  delete     - 删除文章")
            print("  validate   - 验证所有文章格式")
            print("  stats      - 显示统计信息")
            print("\n或直接运行命令:")
            print("  python scripts/manage_posts.py list")
            print("=" * 50)
            command = input("\n请选择命令 (list/delete/validate/stats): ").strip().lower()
        
        if command == 'list':
            list_articles(config)
        elif command == 'delete':
            delete_article(config)
        elif command == 'validate':
            validate_all_articles(config)
        elif command == 'stats':
            show_statistics(config)
        else:
            print(f"❌ 未知命令: {command}")
            sys.exit(1)
    
    except SiteBuilderError as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ 已取消")
        sys.exit(1)


if __name__ == "__main__":
    main()
