"""文件操作工具函数"""

from pathlib import Path
from typing import Optional
import shutil


def ensure_dir(directory: Path) -> Path:
    """确保目录存在，如果不存在则创建"""
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def copy_static_files(source: Path, destination: Path) -> None:
    """复制静态文件目录"""
    if not source.exists():
        return
    
    if destination.exists():
        shutil.rmtree(destination)
    
    shutil.copytree(source, destination)


def get_relative_path(file_path: Path, base_path: Path) -> str:
    """获取相对路径字符串"""
    try:
        return str(file_path.relative_to(base_path))
    except ValueError:
        return str(file_path)
