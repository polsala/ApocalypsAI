FROM alpine/git:latest

WORKDIR /app

COPY src/critter_catcher.sh /usr/local/bin/critter_catcher.sh

RUN chmod +x /usr/local/bin/critter_catcher.sh

ENTRYPOINT ["/usr/local/bin/critter_catcher.sh"]
