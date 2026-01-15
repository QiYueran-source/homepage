#!/usr/bin/env python3
"""
静态网站构建脚本（重构版）
使用模块化架构，易于维护和扩展
"""

from pathlib import Path
import sys

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.builders.site_builder import SiteBuilder
from src.utils.exceptions import SiteBuilderError


def main():
    """主函数"""
    try:
        # 加载配置
        config = Config()
        
        # 创建构建器并构建网站
        builder = SiteBuilder(config)
        builder.build()
        
    except SiteBuilderError as e:
        print(f"❌ 构建失败: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ 构建已取消", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 未知错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
