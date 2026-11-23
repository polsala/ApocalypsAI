FROM alpine:3.18

# Install bash for script execution
RUN apk add --no-cache bash

COPY src/quote.sh /usr/local/bin/quote.sh
RUN chmod +x /usr/local/bin/quote.sh

ENTRYPOINT ["/usr/local/bin/quote.sh"]
