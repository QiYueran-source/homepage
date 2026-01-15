#!/bin/bash
# Docker 部署脚本
# 用于正确启动容器，确保端口映射正确

set -e

echo "🚀 开始部署..."

# 停止并删除旧容器（如果存在）
if [ "$(docker ps -aq -f name=ltw)" ]; then
    echo "停止并删除旧容器..."
    docker stop ltw 2>/dev/null || true
    docker rm ltw 2>/dev/null || true
fi

# 如果使用 docker-compose
if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
    echo "使用 docker-compose 启动..."
    docker-compose down 2>/dev/null || docker compose down 2>/dev/null || true
    docker-compose up -d --build || docker compose up -d --build
    echo "✅ 部署完成！"
    echo "访问地址: http://服务器IP:8080"
    exit 0
fi

# 如果使用 docker 命令
echo "使用 docker 命令启动..."

# 检查镜像是否存在
if ! docker images | grep -q "ltw-website"; then
    echo "构建镜像..."
    docker build -t ltw-website .
fi

# 启动容器，确保端口映射正确：主机8080 -> 容器82
echo "启动容器..."
docker run -d \
    -p 0.0.0.0:8080:82 \
    --name ltw \
    --restart unless-stopped \
    ltw-website

# 验证端口映射
echo ""
echo "验证端口映射..."
docker port ltw

echo ""
echo "✅ 部署完成！"
echo "容器名称: ltw"
echo "访问地址: http://服务器IP:8080"
echo ""
echo "查看日志: docker logs -f ltw"
echo "停止容器: docker stop ltw"
echo "重启容器: docker restart ltw"
