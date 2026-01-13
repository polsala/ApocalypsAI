FROM alpine:3.20
WORKDIR /app
COPY src/main.sh /app/main.sh
COPY src/quotes.txt /app/quotes.txt
RUN chmod +x /app/main.sh
ENTRYPOINT ["./main.sh"]
