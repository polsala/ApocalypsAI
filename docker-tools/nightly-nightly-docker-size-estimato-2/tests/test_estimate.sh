#!/usr/bin/env sh
set -e

# Create a temporary Dockerfile for testing
cat > /tmp/Dockerfile.test <<'EOF'
FROM alpine:3.18
RUN apk add --no-cache curl
COPY . /app
RUN echo "done"
EOF

EXPECTED="26 MB"
OUTPUT=$(./src/estimate_size.sh /tmp/Dockerfile.test)

if [ "$OUTPUT" = "$EXPECTED" ]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: expected $EXPECTED but got $OUTPUT"
  exit 1
fi
