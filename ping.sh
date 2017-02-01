#!/bin/bash

./build.sh
./run.sh

while [ true ]
do
  sleep 1
  echo " "; echo " "
  curl localhost:5000
  echo " "; echo " "
  curl localhost:8080/service-instances/microservice
  echo " "; echo " "
  curl -H "accept: application/json" localhost:8888/uaa/login
done

