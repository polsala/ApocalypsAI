FROM alpine:latest

# Install bash for the script
RUN apk add --no-cache bash

WORKDIR /app

# Copy the script
COPY src/dust_bunny_sweeper.sh .

# Make the script executable
RUN chmod +x dust_bunny_sweeper.sh

# Entrypoint to run the script
ENTRYPOINT ["./dust_bunny_sweeper.sh"]
CMD ["--help"] # Default to showing help
