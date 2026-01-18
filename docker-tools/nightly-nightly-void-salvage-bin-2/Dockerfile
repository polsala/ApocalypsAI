FROM alpine:latest

RUN apk add --no-cache openssl bash

WORKDIR /app

COPY src/entry.sh .
RUN chmod +x entry.sh

ENTRYPOINT ["./entry.sh"]
