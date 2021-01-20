#!/bin/bash

mkdir -p ./mongodb/data/log/
#touch ./mongodb/data/log/mongod.log
#chown -R root:root ./mongodb
mkdir -p ./django/logs/
docker-compose up -d
