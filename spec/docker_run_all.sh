#!/bin/bash

docker run -d \
  --name benchmark-java-benchmark-java-2 \
  --network benchmark-java_default \
  -p 8085:8080 \
  -e SPRING_DATASOURCE_URL=jdbc:postgresql://db-java:5432/benchmark \
  -e SPRING_DATASOURCE_USERNAME=benchmark \
  -e SPRING_DATASOURCE_PASSWORD=benchmark \
  benchmark-java-benchmark-java:latest

docker run -d \
    --name benchmark-csharp-benchmark-csharp-2 \
    --network benchmark-csharp_default \
    -p 8086:8080 \
    -e 'ConnectionStrings__DefaultConnection=Host=db-csharp;Database=benchmark;Username=benchmark;Password=benchmark' \
    benchmark-csharp-benchmark-csharp:latest

docker run -d \
  --name benchmark-python-benchmark-python-2 \
  --network benchmark-python_default \
  -p 8087:8000 \
  -e POSTGRES_DB=benchmark \
  -e POSTGRES_USER=benchmark \
  -e POSTGRES_PASSWORD=benchmark \
  -e POSTGRES_HOST=db-python \
  -e POSTGRES_PORT=5432 \
  benchmark-python-benchmark-python:latest

docker run -d \
  --name benchmark-php-benchmark-php-2 \
  --network benchmark-php_default \
  -p 8088:80 \
  -e DB_CONNECTION=pgsql \
  -e DB_HOST=db-php \
  -e DB_PORT=5432 \
  -e DB_DATABASE=benchmark \
  -e DB_USERNAME=benchmark \
  -e DB_PASSWORD=benchmark \
  -e APP_ENV=production \
  -e LOG_CHANNEL=stderr \
  -e LOG_LEVEL=error \
  benchmark-php-benchmark-php:latest
