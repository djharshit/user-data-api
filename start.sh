#!/bin/bash

if docker network ls | awk '{print $2}' | grep -q "interCon"; then
        echo "Network found"
else
        echo "Not found, creating network"
        docker network create interCon
fi

docker build -t apiserver .

docker run -d -p 27017:27017 --network=interCon mongo
docker run -d -p 5000:5000 --network=interCon apiserver

docker ps -a