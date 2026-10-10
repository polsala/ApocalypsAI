FROM alpine:3.18
RUN apk add --no-cache bash
COPY src/tip.sh /usr/local/bin/tip.sh
RUN chmod +x /usr/local/bin/tip.sh
ENTRYPOINT ["/usr/local/bin/tip.sh"]
