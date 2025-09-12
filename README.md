# AnimeScrapyV2

AnimeWebV2 是一个基于 Flask 的动漫信息展示网站，用于浏览、搜索动漫数据。

## 功能特性

1. **首页展示** - 展示当日热门动漫
2. **动漫库** - 按年份、季度和最低投票数筛选动漫
3. **搜索功能** - 根据关键字搜索动漫
4. **详情页面** - 展示动漫详细信息
5. **图片服务** - 内部图片服务支持
6. **缓存机制** - 使用 Flask-Caching 提高性能
7. **限流功能** - 使用 Flask-Limiter 防止滥用
8. **响应式设计** - 适配不同设备屏幕

## 技术栈

- 后端框架：Flask 3.1.2
- ORM：SQLAlchemy 2.0.43
- 数据库：MariaDB (通过 PyMySQL 驱动)
- 前端：HTML + CSS + JavaScript (无框架)
- 模板引擎：Jinja2 (Flask 默认)
- 部署：Gunicorn + Gevent

## 项目结构

```
AnimeWebV2/
├── app.py              # 应用主文件，定义路由和错误处理
├── model.py            # 数据模型定义
├── service.py          # 业务逻辑处理
├── data.py             # 数据传输对象定义
├── constant.py         # 常量配置
├── config.py           # Gunicorn 配置
├── requirements.txt    # 项目依赖
├── Dockerfile          # Docker 部署配置
├── static/             # 静态资源文件
│   ├── css/            # 样式文件
│   └── js/             # JavaScript 文件
├── templates/          # HTML 模板文件
└── picture/            # 本地图片存储目录
```

## 环境要求

- Python 3.11+
- MariaDB 数据库

## 安装与运行

### 本地开发环境

1. 克隆项目代码：
   ```bash
   git clone <repository-url>
   cd AnimeScrapyV2/AnimeWebV2
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 配置数据库：
   - 在 MySQL 中创建数据库
   - 修改 [constant.py](file:///D:/poject/AnimeScrapyV2/AnimeWebV2/constant.py) 中的数据库连接配置

4. 运行应用：
   ```bash
   python app.py
   ```

### Docker 部署

1. 构建 Docker 镜像：
   ```bash
   docker build -t anime_web:version .
   ```

2. 运行容器：
   ```bash
   docker run -d -p 8000:8000 --name anime_web anime_web:version
   ```

## 配置说明

项目配置主要在 [constant.py](file:///D:/poject/AnimeScrapyV2/AnimeWebV2/constant.py) 文件中：

- `USERNAME`: 数据库用户名
- `PASSWORD`: 数据库密码
- `HOST`: 数据库主机地址
- `PORT`: 数据库端口
- `ENABLE_INNER_PICTURE`: 是否启用内部图片服务
- `PICTURE_PATH`: 图片存储路径
- `SERVER_PORT`: 服务器端口

## API 接口

- `/` - 首页，展示热门动漫
- `/library` - 动漫库，默认显示当前季度动漫
- `/library/<year>/<season>/<vote>` - 按条件筛选动漫库
- `/search` - 搜索动漫
- `/detail/<aid>` - 动漫详情页
- `/picture/<pid>` - 内部图片服务（当启用时）

## 缓存与限流

项目使用 Flask-Caching 进行缓存，Flask-Limiter 进行限流：

- 首页缓存 5 分钟
- 动漫库和搜索页面缓存 1 分钟
- 动漫详情页缓存 1 分钟
- 搜索接口限流：3次/秒，20次/分钟
- 动漫库接口限流：30次/分钟
