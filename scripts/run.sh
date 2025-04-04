#!/bin/bash
set -eo pipefail

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

rollback() {
    log "执行回滚操作"
    docker start web || true
    docker start nginx || true
    docker exec nginx sh -c 'if [ -f /etc/nginx/conf.d/default.conf.bak ]; then \
        cp -f /etc/nginx/conf.d/default.conf.bak /etc/nginx/conf.d/default.conf && \
        nginx -t && nginx -s reload; fi' || true
}

trap rollback ERR

log "=== 开始维护流程 ==="

check_container() {
    if [ "$(docker inspect -f '{{.State.Running}}' "$1")" != "true" ]; then
        log "错误：容器 $1 未运行！"
        exit 1
    fi
}

check_container web
check_container nginx

log "切换Nginx到维护模式..."
docker exec nginx sh -c ' \
    cp /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak && \
    echo -e "server {\n\
        listen 80 default_server;\n\
        server_name _;\n\
        root /usr/share/nginx/maintenance_page;\n\
        location / {\n\
            try_files \$uri \$uri/ /index.html;\n\
        }\n\
    }" > /etc/nginx/conf.d/default.conf && \
    nginx -t && nginx -s reload \
'

log "停止Django容器..."
docker stop web

log "启动爬虫任务..."
docker exec scrapy_container scrapy crawl cars-data

log "启动Django服务..."
docker start web
sleep 15  # 延长等待时间确保Django完全就绪

log "恢复Nginx配置..."
docker exec nginx sh -c ' \
    mv /etc/nginx/conf.d/default.conf.bak /etc/nginx/conf.d/default.conf && \
    nginx -t && \
    nginx -s reload \
'

log "=== 维护流程完成 ==="
