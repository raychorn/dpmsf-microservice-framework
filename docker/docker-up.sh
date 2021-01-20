#!/bin/bash

mkdir -p ./mongodb/data/log/
#touch ./mongodb/data/log/mongod.log
sudo chown -R root:root ./mongodb
sudo chmod -R 0777 ./mongodb
mkdir -p ./django/logs/
sudo chown -R root:root ./django
sudo chmod -R 0777 ./django
docker-compose up -d
