#!/bin/bash

ARRAY=()
ARRAY+=("mongodb")
ARRAY+=("vyperapi")

PS3="Choose: " 

select option in "${ARRAY[@]}";
do
    echo "Choose: $REPLY"
    choice=${ARRAY[$REPLY-1]}
    break
done

CID=$(docker ps -qf "name=$choice")
echo "CID=$CID"
if [[ ! $CID. == . ]]
then
    echo "Showing logs $CID"
    docker logs --tail 2500 $CID
fi
