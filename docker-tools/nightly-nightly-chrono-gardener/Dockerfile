FROM alpine:latest
RUN apk add --no-cache docker-cli bash
COPY src/gardener.sh /usr/local/bin/gardener.sh
RUN chmod +x /usr/local/bin/gardener.sh
ENTRYPOINT ["/usr/local/bin/gardener.sh"]
