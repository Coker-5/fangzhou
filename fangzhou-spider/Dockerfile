# 使用官方 Python 基础镜像
FROM python:3.9-slim

LABEL authors="Wnn"

# 设置容器内工作目录
WORKDIR /app

# 安装系统依赖（包含字体库，用于词云生成）
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libfreetype6 \
    && rm -rf /var/lib/apt/lists/*

# 复制 requirements 文件先执行，利用 Docker 缓存优化
COPY ./requirements.txt .

# 安装 Python 依赖（包含 Scrapy、pymongo 和词云库）
RUN pip install --no-cache-dir -r requirements.txt

# 复制整个项目到容器中（注意 .dockerignore 需要排除不必要的文件）
COPY . .

# 创建日志和词云输出目录（与挂载点保持一致）
RUN mkdir -p /app/logs

#启动爬虫
CMD ["tail", "-f", "/dev/null"]

