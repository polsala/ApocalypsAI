FROM alpine:3.18
RUN apk add --no-cache bash
COPY src/run.sh /usr/local/bin/rot13
RUN chmod +x /usr/local/bin/rot13
ENTRYPOINT ["rot13"]
