FROM alpine:3.18

# Install bash (Alpine ships with ash, we need bash for $RANDOM handling)
RUN apk add --no-cache bash

# Copy the generator script
COPY src/generate.sh /usr/local/bin/generate.sh
RUN chmod +x /usr/local/bin/generate.sh

# Set entrypoint
ENTRYPOINT ["bash", "/usr/local/bin/generate.sh"]
