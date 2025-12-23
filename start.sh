#!/bin/bash

CONTAINER_NAME="my-postgres"
HOST_PORT=5433
DB_PORT=5432

# Check if container exists
if [ $(docker ps -a -q -f name=$CONTAINER_NAME) ]; then
    echo "Container $CONTAINER_NAME already exists. Removing..."
    docker rm -f $CONTAINER_NAME
fi

# Run new PostgreSQL container in detached mode
echo "Starting PostgreSQL container..."
docker run -d \
  --name $CONTAINER_NAME \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=mydb \
  -p $HOST_PORT:$DB_PORT \
  postgres:15

# Attach to the container's bash shell
echo "Attaching to $CONTAINER_NAME..."
docker exec -it $CONTAINER_NAME bash

