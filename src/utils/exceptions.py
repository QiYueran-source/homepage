"""自定义异常类"""


class SiteBuilderError(Exception):
    """网站构建器基础异常"""
    pass


class ConfigError(SiteBuilderError):
    """配置错误"""
    pass


class LoaderError(SiteBuilderError):
    """数据加载错误"""
    pass


class BuilderError(SiteBuilderError):
    """构建器错误"""
    pass


class ValidationError(SiteBuilderError):
    """数据验证错误"""
    pass
