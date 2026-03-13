FROM alpine:latest

LABEL maintainer="ApocalypsAI Community"
LABEL org.opencontainers.image.description="Minimal survival container with diagnostic tools"

RUN apk add --no-cache \
  curl \
  wget \
  iputils \
  bind-tools \
  tcpdump \
  strace \
  htop \
  vim \
  bash

CMD ["/bin/bash"]
