#!/bin/bash

set -e

LANG_PRESET=${1:-python}
DEVBOX_DIR=".devbox"

mkdir -p $DEVBOX_DIR

cat > $DEVBOX_DIR/Dockerfile << 'EOF'
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
  curl \
  git \
  sudo \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
EOF

cat > $DEVBOX_DIR/docker-compose.yml << EOF
version: '3.8'
services:
  devbox:
    build:
      context: .
      dockerfile: $DEVBOX_DIR/Dockerfile
    volumes:
      - ..:/workspace
    ports:
      - "8080:8080"
    stdin_open: true
    tty: true
    environment:
      - LANG_PRESET=$LANG_PRESET
EOF

cat > $DEVBOX_DIR/entrypoint.sh << 'EOF'
#!/bin/bash
set -e

echo "Booting devbox with preset: $LANG_PRESET"

# Install language-specific tooling
if [ "$LANG_PRESET" = "python" ]; then
  apt-get update && apt-get install -y python3 python3-pip python3-venv
  python3 -m venv /opt/venv
  export PATH="/opt/venv/bin:$PATH"
  echo "Python devbox ready."
elif [ "$LANG_PRESET" = "node" ]; then
  curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
  apt-get install -y nodejs
  echo "Node.js devbox ready."
elif [ "$LANG_PRESET" = "go" ]; then
  curl -LO https://go.dev/dl/go1.21.0.linux-amd64.tar.gz
  tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz
  export PATH=$PATH:/usr/local/go/bin
  echo "Go devbox ready."
elif [ "$LANG_PRESET" = "rust" ]; then
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
  source "$HOME/.cargo/env"
  echo "Rust devbox ready."
fi

exec "$@"
EOF

chmod +x $DEVBOX_DIR/entrypoint.sh

echo "Devbox initialized for $LANG_PRESET in $DEVBOX_DIR"
echo "Run: cd $DEVBOX_DIR && docker-compose run --rm devbox bash"
