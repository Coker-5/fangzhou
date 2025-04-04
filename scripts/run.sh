#!/bin/bash
# 强制错误退出
set -eo pipefail

# 日志记录函数
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# 定义恢复函数
rollback() {
    log "执行回滚操作"
    docker start web || true
    docker exec nginx sh -c '[[ -f /etc/nginx/nginx.conf.bak ]] && mv /etc/nginx/nginx.conf.bak /etc/nginx/nginx.conf && nginx -s reload' || true
}

# 注册错误处理
trap rollback ERR

log "=== 开始维护流程 ==="

# 停止Django服务
log "停止Django容器..."
docker stop web

# 切换Nginx到维护模式
log "切换Nginx配置..."
docker exec nginx cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
docker exec nginx sed -i 's#proxy_pass http://web:8000;#root /usr/share/nginx/maintenance_page;#g' /etc/nginx/nginx.conf
docker exec nginx nginx -s reload

# 执行爬虫（关键修改点）
log "启动爬虫任务..."
if ! docker exec scrapy_container scrapy crawl your_spider; then
    log "爬虫执行失败！错误码: $?"
    exit 1
fi

# 恢复服务

log "启动Django服务..."
docker start web

log "恢复Nginx配置..."
docker exec nginx mv /etc/nginx/nginx.conf.bak /etc/nginx/nginx.conf
docker exec nginx nginx -s reload



log "=== 维护流程完成 ==="