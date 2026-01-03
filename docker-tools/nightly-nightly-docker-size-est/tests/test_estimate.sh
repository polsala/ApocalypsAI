#!/usr/bin/env sh
set -e

# Create a temporary Dockerfile
cat > /tmp/Dockerfile.test <<'EOF'
FROM alpine:3.18
RUN apk add --no-cache curl
COPY . /app
EOF

# Run the estimator
OUTPUT=$(../src/estimate.sh /tmp/Dockerfile.test)

# Expected size: base 5 + RUN 10 + COPY 1 = 16MB
EXPECTED="16MB"

if [ "$OUTPUT" = "$EXPECTED" ]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: expected $EXPECTED but got $OUTPUT"
  exit 1
fi
