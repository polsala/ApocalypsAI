FROM alpine:latest
RUN apk add --no-cache docker-cli bash
COPY src/wrangler.sh /usr/local/bin/wrangler.sh
RUN chmod +x /usr/local/bin/wrangler.sh
ENTRYPOINT ["/usr/local/bin/wrangler.sh"]
