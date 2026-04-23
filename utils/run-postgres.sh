#!/bin/bash

CONTAINER_NAME="pipeline_postgres"

if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "Container already exists. Starting it..."
  docker start "$CONTAINER_NAME"
else
  echo "Creating PostgreSQL container..."
  docker run -d \
    -e POSTGRES_USER=pipeline_user \
    -e POSTGRES_PASSWORD=strongpassword \
    -e POSTGRES_DB=pipeline_db \
    -p 5433:5432 \
    --name "$CONTAINER_NAME" \
    postgres:15
fi