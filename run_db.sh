#!/usr/bin/env bash
docker rm -f -v postgres_udacity
docker run --name postgres_udacity -v volume_postgres:/data/db -h 127.0.0.1 -p 5432:5432 -e POSTGRES_USER=student -e POSTGRES_PASSWORD=student -e POSTGRES_DB=studentdb -d postgres:latest
sleep 5