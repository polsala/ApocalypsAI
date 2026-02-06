FROM alpine:3.18
WORKDIR /app
COPY src/portal.sh .
RUN chmod +x portal.sh
ENTRYPOINT ["./portal.sh"]
