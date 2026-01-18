FROM alpine:latest

RUN apk add --no-cache bash tar

COPY src/salvage.sh /usr/local/bin/salvage.sh
RUN chmod +x /usr/local/bin/salvage.sh

WORKDIR /data

ENTRYPOINT ["salvage.sh"]
