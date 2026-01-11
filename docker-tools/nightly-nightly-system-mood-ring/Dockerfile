FROM alpine:latest

RUN apk add --no-cache bash procps coreutils

WORKDIR /app

COPY src/mood_ring.sh /app/mood_ring.sh

RUN chmod +x /app/mood_ring.sh

CMD ["/app/mood_ring.sh"]
