# 静态网站生成器

一个模块化、可维护的静态网站生成器，用于从 YAML 和 Markdown 文件生成个人网站和博客。

## 特性

- 📝 **博客系统**：支持多分类博客，自动生成文章详情页
- 🎨 **现代设计**：简洁优雅的博客风格界面
- 🔧 **模块化架构**：清晰的代码结构，易于维护和扩展
- ⚙️ **配置管理**：统一的配置文件管理
- 🛠️ **工具脚本**：文章创建和管理工具
- 📦 **类型提示**：完整的类型注解，提升代码质量

## 项目结构

```
/home/ltw/files/ltw/
├── src/                    # 源代码目录
│   ├── config.py          # 配置管理
│   ├── models/            # 数据模型
│   ├── loaders/           # 数据加载器
│   ├── processors/        # 数据处理器
│   ├── builders/          # 构建器
│   └── utils/             # 工具函数
├── config/                # 配置文件
│   ├── settings.yaml      # 主配置
│   └── category_mapping.yaml  # 分类映射
├── data/                  # 数据文件
│   ├── blog/             # 博客文章
│   └── *.yaml            # 其他数据文件
├── templates/             # Jinja2 模板
├── dist/                  # 构建输出目录
├── scripts/               # 工具脚本
│   ├── new_post.py       # 创建新文章
│   └── manage_posts.py   # 文章管理
└── build.py               # 构建入口

```

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 构建网站

```bash
python build.py
```

构建后的文件将输出到 `dist/` 目录。

### 创建新文章

```bash
python scripts/new_post.py
```

交互式创建新博客文章，自动生成 frontmatter 和文件。

### 管理文章

```bash
# 列出所有文章
python scripts/manage_posts.py list

# 删除文章
python scripts/manage_posts.py delete

# 验证文章格式
python scripts/manage_posts.py validate

# 显示统计信息
python scripts/manage_posts.py stats
```

## Docker 部署

### 使用 Docker 构建和运行

#### 方式一：使用 Docker Compose（推荐）

```bash
# 构建并启动容器
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止容器
docker-compose down
```

网站将在 `http://localhost:8080` 访问。

#### 方式二：使用 Docker 命令

```bash
# 构建镜像
docker build -t ltw-website .

# 运行容器（注意：容器内端口是 82）
docker run -d -p 8080:82 --name ltw-website --restart unless-stopped ltw-website

# 查看日志
docker logs -f ltw-website

# 停止容器
docker stop ltw-website

# 删除容器
docker rm ltw-website
```

#### 方式三：使用部署脚本（推荐）

```bash
# 给脚本添加执行权限
chmod +x deploy.sh

# 运行部署脚本
./deploy.sh
```

脚本会自动处理容器启动和端口映射配置。

### Docker 配置说明

- **Dockerfile**: 多阶段构建，先使用 Python 构建静态网站，然后使用 Nginx 提供服务
- **nginx.conf**: Nginx 配置文件，包含 gzip 压缩、静态资源缓存等优化
- **docker-compose.yml**: Docker Compose 配置文件，简化部署流程
- **.dockerignore**: 排除不需要的文件，减小镜像体积

### 服务器部署注意事项

1. **端口映射**：确保使用 `-p 8080:82`（主机端口:容器端口），不要使用 `127.0.0.1` 绑定
2. **防火墙**：开放服务器防火墙的 8080 端口
3. **安全组**：在云服务器控制台的安全组中开放 8080 端口的入站规则

**正确的启动命令：**
```bash
docker run -d -p 0.0.0.0:8080:82 --name ltw --restart unless-stopped ltw-website
```

**错误的启动命令（只能本地访问）：**
```bash
docker run -d -p 127.0.0.1:82:8080 --name ltw ltw-website  # ❌ 错误
```

### 自定义端口

在 `docker-compose.yml` 中修改端口映射：

```yaml
ports:
  - "3000:82"  # 将 3000 改为你想要的端口（容器内是 82）
```

或使用 Docker 命令：

```bash
docker run -d -p 3000:82 --name ltw-website ltw-website
```

## 配置

### 主配置文件

编辑 `config/settings.yaml` 来修改路径和其他设置：

```yaml
paths:
  data: "data"
  templates: "templates"
  dist: "dist"
  static: "static"

blog:
  categories_file: "config/category_mapping.yaml"
  default_image: "https://picsum.photos/seed/{slug}/800/500"

build:
  encoding: "utf-8"
  auto_create_dirs: true
```

### 分类映射

编辑 `config/category_mapping.yaml` 来添加或修改分类的中文名称：

```yaml
tech-notes: "技术笔记"
finance: "经济金融"
essays: "个人随想"
```

## 架构设计

### 模块说明

- **config.py**: 配置管理，统一加载和管理配置
- **models/**: 数据模型，使用 dataclass 定义数据结构
- **loaders/**: 数据加载器，负责加载 YAML 和 Markdown 文件
- **processors/**: 数据处理器，处理 slug 生成、分类映射等
- **builders/**: 构建器，负责页面渲染和文件生成
- **utils/**: 工具函数，文件操作、验证等通用功能

### 设计原则

1. **单一职责**：每个模块/类只负责一个功能
2. **DRY原则**：消除代码重复
3. **依赖注入**：通过配置和参数传递依赖
4. **错误处理**：统一的异常处理机制
5. **类型提示**：完整的类型注解

## 开发

### 代码规范

- 遵循 PEP 8
- 使用类型提示
- 编写文档字符串

### 扩展功能

1. **添加新页面**：在 `templates/` 创建模板，在 `SiteBuilder` 中添加构建逻辑
2. **添加新数据源**：创建新的 Loader 类
3. **添加新处理器**：在 `processors/` 中添加处理逻辑

## 许可证

MIT License
