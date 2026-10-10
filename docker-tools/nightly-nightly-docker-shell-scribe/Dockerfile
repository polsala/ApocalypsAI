FROM alpine:3.18

WORKDIR /app

COPY src/scribe.sh /usr/local/bin/scribe.sh

RUN chmod +x /usr/local/bin/scribe.sh

RUN mkdir -p /app/vault

ENTRYPOINT ["scribe.sh"]
