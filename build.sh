echo "Build Mode: ${1}"

if [ ${1} = "dev" ]; then
    docker compose -f docker-compose.dev.yaml up -d --build --remove-orphans
elif [ ${1} = "prod" ]; then
    docker compose -f docker-compose.prod.yaml up -d --build --remove-orphans
fi
