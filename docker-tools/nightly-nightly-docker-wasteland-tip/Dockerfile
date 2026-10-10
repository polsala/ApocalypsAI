FROM alpine:3.18
WORKDIR /app
COPY src/tips.sh /app/tips.sh
RUN chmod +x /app/tips.sh
ENTRYPOINT ["/app/tips.sh"]
