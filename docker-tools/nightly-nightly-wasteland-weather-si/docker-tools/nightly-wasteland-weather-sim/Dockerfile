FROM alpine:3.18
RUN apk add --no-cache bash coreutils
COPY src/weather.sh /usr/local/bin/weather.sh
RUN chmod +x /usr/local/bin/weather.sh
ENTRYPOINT ["/usr/local/bin/weather.sh"]
