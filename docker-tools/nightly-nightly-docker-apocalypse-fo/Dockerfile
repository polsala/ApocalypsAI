FROM alpine:3.18

WORKDIR /app

COPY src/ /app/

RUN chmod +x fortune.sh

ENTRYPOINT ["./fortune.sh"]
