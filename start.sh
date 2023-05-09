#!/bin/bash

if docker network ls | awk '{print $2}' | grep -q "mynet"; then
        echo "Network found"
else
        echo "Not found, creating network"
        docker network create mynet
fi

if docker volume ls | awk '{print $2}' | grep -q "mongovol"; then
        echo "volume found"
else
        echo "Not found, creating volume"
        docker volume create mongovol
fi

docker run -d -p 27017:27017 -v mongovol:/data/db --network=mynet mongo

docker ps -a