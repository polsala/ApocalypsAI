FROM alpine:3.18
WORKDIR /app
COPY src/ .
RUN chmod +x tip.sh
ENTRYPOINT ["./tip.sh"]
