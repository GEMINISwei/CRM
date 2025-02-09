echo "Build Mode: ${1}"

if [ ${1} = "dev" ]; then
    docker compose -f docker-compose.dev.yaml up -d --build --remove-orphans
elif [ ${1} = "prod" ]; then
    docker compose -f docker-compose.prod.yaml up -d --build --remove-orphans

    # 編譯完成後, 需將前端產出之靜態網頁放置 Nginx Html 資料夾
    rm -rf ./Service/Frontend/dist
    docker cp crm-frontend-1:/app/dist ./Service/Frontend/dist

    # 放完後直接刪除, 不需要留著
    docker container rm crm-frontend-1
    docker system prune
fi
