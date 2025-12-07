FROM docker:24.0
WORKDIR /app
COPY src/weeder.sh ./
RUN chmod +x weeder.sh
ENTRYPOINT ["./weeder.sh"]
