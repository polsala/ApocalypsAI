FROM alpine:latest

WORKDIR /app

COPY src/sweeper.sh /usr/local/bin/sweeper.sh

RUN chmod +x /usr/local/bin/sweeper.sh

ENTRYPOINT ["/usr/local/bin/sweeper.sh"]
CMD ["--help"]
