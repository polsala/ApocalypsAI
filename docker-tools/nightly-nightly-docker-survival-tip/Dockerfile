FROM alpine:3.18
WORKDIR /app
COPY src/tip.sh .
RUN chmod +x tip.sh
ENTRYPOINT ["./tip.sh"]
