#!/bin/bash

if [ ! -f .env ]
then
    export $(cat .env | xargs)
fi

mongo --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD  --authenticationDatabase $MONGO_INITDB_DATABASE --host 10.5.0.5 --port 27017
