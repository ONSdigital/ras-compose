FROM alpine

# Inspired by https://github.com/byrnedo/docker-alpine-curl
MAINTAINER David Carboni

RUN apk add --update curl && \
    rm -rf /var/cache/apk/*

ENTRYPOINT ["/bin/sh"]
