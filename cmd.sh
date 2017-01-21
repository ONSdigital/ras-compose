#!/bin/bash

# Buid Alpine image with curl 
# (this will use cached layers, so is quick to run after an initial build)
docker build --tag cmd curl/
# docker build --no-cache --tag cmd curl/

# Start an interactive shell in a container connected to the network that docker-compose will create
echo - You should be able to run curl commands from here to the components.
docker run -it --rm --name cmd --net rascompose_ras cmd
