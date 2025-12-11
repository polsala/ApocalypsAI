FROM alpine:latest

# Install bash for the script
RUN apk add --no-cache bash

WORKDIR /app

COPY src/dust_bunny_sweeper.sh .

RUN chmod +x dust_bunny_sweeper.sh

ENTRYPOINT ["./dust_bunny_sweeper.sh"]
