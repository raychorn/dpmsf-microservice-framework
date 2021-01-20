#!/bin/bash

vyperapi="vyperapi"

mkdir -p ./mongodb/data/log/
#touch ./mongodb/data/log/mongod.log
sudo chown -R root:root ./mongodb
sudo chmod -R 0777 ./mongodb
mkdir -p ./django/logs/
sudo chown -R root:root ./django
sudo chmod -R 0777 ./django
docker-compose up -d
sleep 15s
CID=$(docker ps -qf "name=$vyperapi")
echo "CID=$CID"
if [[ ! $CID. == . ]]
then
    echo "Restarting $CID"
    docker restart $CID
fi
service nginx restart