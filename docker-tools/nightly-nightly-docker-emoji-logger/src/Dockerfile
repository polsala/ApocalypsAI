FROM alpine:3.20
RUN apk add --no-cache bash
COPY src/main.sh /usr/local/bin/emoji-logger
RUN chmod +x /usr/local/bin/emoji-logger
ENTRYPOINT ["emoji-logger"]
