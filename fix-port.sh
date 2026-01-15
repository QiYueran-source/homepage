#!/bin/bash
# 快速修复端口映射问题
# 在服务器上运行此脚本

echo "🔧 修复端口映射..."

# 停止并删除当前容器
if [ "$(docker ps -aq -f name=ltw)" ]; then
    echo "停止容器 ltw..."
    docker stop ltw
    docker rm ltw
    echo "✅ 旧容器已删除"
fi

# 使用正确的端口映射重新启动
echo "使用正确的端口映射启动容器..."
docker run -d \
    -p 0.0.0.0:8080:82 \
    --name ltw \
    --restart unless-stopped \
    1:latest

# 验证
echo ""
echo "验证端口映射："
docker port ltw

echo ""
echo "✅ 修复完成！"
echo "现在可以通过 http://服务器IP:8080 访问"
echo ""
echo "如果仍无法访问，请检查："
echo "1. 云服务器安全组是否开放 8080 端口"
echo "2. 服务器防火墙: sudo ufw allow 8080/tcp"
