FROM alpine:3.18
WORKDIR /app
COPY src/estimate_size.sh /estimate_size.sh
RUN chmod +x /estimate_size.sh
ENTRYPOINT ["/estimate_size.sh"]
