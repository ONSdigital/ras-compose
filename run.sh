#!/bin/bash

# Start containers
docker-compose down
docker-compose build
docker-compose up -d

# Scale up services to create a cluster
#docker-compose scale spring-eureka=3
#docker-compose scale spring-config=3
#docker-compose scale spring-client=2

docker-compose ps
