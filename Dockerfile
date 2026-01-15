# 多阶段构建 Dockerfile
# 第一阶段：构建静态网站
FROM python:3.10-slim as builder

# 设置工作目录
WORKDIR /app

# 配置 apt 使用国内镜像源（阿里云）加速下载
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || \
    sed -i 's|http://deb.debian.org|http://mirrors.aliyun.com|g' /etc/apt/sources.list 2>/dev/null || true

# 这些 Python 包都是纯 Python 实现，不需要编译工具
# 如果后续需要编译的包，可以取消下面的注释
# RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# 配置 pip 使用国内镜像源（清华源）
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 构建静态网站
RUN python build.py

# 第二阶段：使用 Nginx 提供静态文件服务
FROM nginx:alpine

# 复制构建好的静态文件到 Nginx 默认目录
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制 Nginx 配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 82

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]
