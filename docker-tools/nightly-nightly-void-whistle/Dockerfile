FROM alpine:latest

RUN apk add --no-cache sox

COPY ./sounds /sounds
COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
