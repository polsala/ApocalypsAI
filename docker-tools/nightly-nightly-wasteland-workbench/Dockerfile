FROM alpine/git:latest

WORKDIR /app

RUN apk add --no-cache jq curl python3 py3-pip

COPY src/entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["/bin/bash"]
