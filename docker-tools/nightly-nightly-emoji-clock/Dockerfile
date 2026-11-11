FROM alpine:3.18

# Install Bash
RUN apk add --no-cache bash

# Copy the script
COPY src/emoji_clock.sh /usr/local/bin/emoji_clock.sh
RUN chmod +x /usr/local/bin/emoji_clock.sh

ENTRYPOINT ["/usr/local/bin/emoji_clock.sh"]
