FROM alpine:3.18
WORKDIR /app
COPY src/tip.sh /app/tip.sh
RUN chmod +x /app/tip.sh
ENTRYPOINT ["/app/tip.sh"]
