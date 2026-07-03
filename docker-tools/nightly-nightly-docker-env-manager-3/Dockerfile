FROM alpine:latest

RUN apk add --no-cache docker-compose

COPY src/docker-env-manager /usr/local/bin/docker-env-manager

RUN chmod +x /usr/local/bin/docker-env-manager

ENTRYPOINT ["docker-env-manager"]
