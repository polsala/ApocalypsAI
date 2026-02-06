#!/bin/sh
set -e
# Build the test image (quiet output)
docker build -t nightly-quote-mixer-test . > /dev/null
# Run the container and capture its output
output=$(docker run --rm nightly-quote-mixer-test)
expected="Fortune favors the bold. — All that glitters is not gold."
if [ "$output" = "$expected" ]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: expected '$expected' got '$output'"
  exit 1
fi
