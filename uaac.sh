#!/bin/bash

# Get the network name:
network=`docker network ls --filter name=ras -q`

# Run a container and capture the ID of the container:
docker run -it --net $network --rm --entrypoint /bin/sh governmentpaas/cf-uaac

Echo Tailing Docker log for $name. Ctrl-C will stop tailing but will leave the container running.
docker logs -f $name
