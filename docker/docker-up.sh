#!/bin/bash

vyperapi="vyperapi" 

mongodb_data_log=./mongodb/data/log/
if [[ ! -d $mongodb_data_log ]]
then
    echo "Created $mongodb_data_log"
    sudo mkdir -p $mongodb_data_log
fi
#touch ./mongodb/data/log/mongod.log
sudo chown -R root:root ./mongodb
sudo chmod -R 0777 ./mongodb

django_logs=./django/logs/
if [[ ! -d $django_logs ]]
then
    echo "Created $django_logs"
    sudo mkdir -p $django_logs
fi
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
        sudo mkdir -p $workspace
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
