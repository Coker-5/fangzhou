# Fangzhou 项目文档

## 项目概述
Fangzhou 是一个集汽车数据爬取、分析、存储和展示于一体的项目。项目主要包含数据爬虫、数据分析、后端服务和前端展示等模块，通过 Docker 容器化部署，确保各个组件的独立性和可扩展性。

## 项目结构
```
fangzhou/
├── fangzhou-backend/  # Django 后端项目
│   └── fangzhou/
│       ├── datashow/  # 数据展示相关视图和模型
│       ├── .idea/     # IDE 配置文件
│       ├── manage.py  # Django 管理脚本
│       └── requirements.txt  # 后端依赖
├── fangzhou-spider/  # Scrapy 爬虫项目
│   └── cars/
│       ├── spiders/   # 爬虫脚本
│       ├── pipelines.py  # 数据处理管道
│       ├── items.py  # 数据项定义
│       ├── data_analysis.py  # 数据分析模块
│       └── requirements.txt  # 爬虫依赖
├── fangzhou-frontend/  # 前端项目（未详细提供代码）
│   └── dist/  # 打包后的前端文件
├── scripts/  # 脚本目录
│   └── run.sh  # 维护脚本
├── .idea/     # IDE 配置文件
├── docker-compose.yml  # Docker 容器编排文件
└── requirements.txt  # 项目总依赖（未详细提供）
```

## 功能模块

### 1. 数据爬虫
- **Scrapy 框架**：使用 Scrapy 框架编写爬虫，从懂车帝汽车数据网站抓取汽车信息。
- **数据提取**：解析汽车列表和详细信息页面，提取品牌、车型、销量、价格等关键数据。
- **数据处理**：在 `pipelines.py` 中对爬取的数据进行清洗和排序，去除缺失值，并按 `rank` 列排序。

### 2. 数据分析
- **数据统计**：在 `data_analysis.py` 中对爬取的数据进行统计分析，包括车辆总数、销量最多的汽车、最高销售额、平均价格等。
- **可视化数据生成**：生成新能源汽车销量排行榜、汽车品牌销售量饼图、汽车销售价格占比等可视化数据。
- **词云生成**：根据汽车品牌和车型生成词云图，并转换为 Base64 编码。

### 3. 后端服务
- **Django 框架**：使用 Django 框架搭建后端服务，提供 API 接口。
- **MongoDB 存储**：使用 `mongoengine` 连接 MongoDB 数据库，存储和管理汽车数据。
- **数据接口**：在 `datashow/views.py` 中定义多个视图函数，提供不同数据的 JSON 接口。

### 4. 前端展示
- **Nginx 代理**：使用 Nginx 作为前端服务器，代理前端静态文件和后端 API 请求。
- **静态页面**：将前端打包后的文件放置在 `fangzhou-frontend/dist` 目录下，通过 Nginx 提供服务。

## 部署说明

### 1. 环境准备
- 安装 Docker 和 Docker Compose
- 确保系统已安装 Python 3.8 及以上版本

### 2. 依赖安装
- **爬虫项目**：进入 `fangzhou-spider` 目录，执行以下命令安装依赖：
```bash
pip install -r requirements.txt
```
- **后端项目**：进入 `fangzhou-backend/fangzhou` 目录，执行以下命令安装依赖：
```bash
pip install -r requirements.txt
```

### 3. 容器部署
- 在项目根目录下，执行以下命令启动 Docker 容器：
```bash
docker-compose up -d
```
- 该命令将启动 Scrapy 爬虫、MongoDB 数据库、Django 后端和 Nginx 前端服务器。

### 4. 维护脚本
- 在 `scripts/run.sh` 中定义了项目的维护流程，包括切换 Nginx 到维护模式、停止 Django 容器、启动爬虫任务、恢复 Nginx 配置等。
- 执行以下命令运行维护脚本：
```bash
sh scripts/run.sh
```

## API 接口说明
### 1. 数据接口
- **`/center_data/`**：返回车辆总数据、销量最多的汽车、最高销售额等信息。
- **`/head/`**：返回汽车数据的统计信息，如总数、文档 ID 等。
- **`/center_left1/`**：返回新能源汽车销量排行榜。
- **`/center_left2/`**：返回汽车品牌和车型的词云图 Base64 编码。
- **`/center_right1/`**：返回汽车品牌销售量饼图数据。
- **`/center_right2/`**：返回汽车销售价格占比数据。
- **`/bottom_left/`**：返回所有汽车数据列表。
- **`/bottom_right/`**：返回静态图片路径。

### 2. 请求示例
```bash
curl http://localhost:8000/center_data/
```

## 注意事项
- 确保 MongoDB 服务正常运行，并且 `docker-compose.yml` 中的连接配置正确。
- 在运行爬虫任务前，确保网络连接正常，并且目标网站允许爬虫访问。
- 维护脚本中的容器名称和路径需要根据实际情况进行调整。

## 贡献指南
如果你想为该项目做出贡献，请遵循以下步骤：
1. Fork 该项目到你的 GitHub 仓库。
2. 创建一个新的分支，进行代码修改和功能开发。
3. 提交 Pull Request，并详细描述你的修改内容和目的。

## 许可证
本项目采用 [MIT 许可证](LICENSE)。
