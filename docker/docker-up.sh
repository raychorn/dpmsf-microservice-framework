#!/bin/bash

vyperapi="vyperapi" 

mkdir -p ./mongodb/data/log/
#touch ./mongodb/data/log/mongod.log
sudo chown -R root:root ./mongodb
sudo chmod -R 0777 ./mongodb
mkdir -p ./django/logs/
sudo chown -R root:root ./django
sudo chmod -R 0777 ./django

ARRAY=()
ARRAY+=('/workspaces/plugins/admin-plugins')

for workspace in "${ARRAY[*]}"
do
    echo "workspace  : $workspace"
    if [[ ! -d $workspace ]]
    then
        echo "Created workspace: $workspace"
        mkdir -p $workspace
    fi
done

docker-compose up -d
sleep 15s

CID=$(docker ps -qf "name=$vyperapi")
echo "CID=$CID"
if [[ ! $CID. == . ]]
then
    echo "vyperapi is running"
    echo "Restarting $CID"
    docker restart $CID
fi
sleep 5s
sudo service nginx restart
sudo service nginx status
