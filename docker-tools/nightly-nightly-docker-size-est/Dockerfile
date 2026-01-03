FROM alpine:3.18
WORKDIR /app
COPY src/estimate.sh /usr/local/bin/estimate.sh
RUN chmod +x /usr/local/bin/estimate.sh
ENTRYPOINT ["/usr/local/bin/estimate.sh"]
