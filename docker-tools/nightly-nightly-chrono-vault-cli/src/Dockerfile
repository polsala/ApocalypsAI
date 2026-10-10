# Use a minimal base image for efficiency
FROM alpine:3.18

# Set a working directory
WORKDIR /app

# Install essential tools
# nano: simple text editor
# coreutils: provides sha256sum (and other basic utilities)
# curl: for network requests
# jq: for JSON processing
# tar: for archiving
# base64: usually part of coreutils or a separate package, explicitly install if needed
RUN apk add --no-cache nano coreutils curl jq tar

# Set default command to bash for interactive use
CMD ["bash"]
