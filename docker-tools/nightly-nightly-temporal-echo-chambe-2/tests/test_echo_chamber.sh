#!/bin/bash

set -euo pipefail

IMAGE_NAME="temporal-echo-chamber-test"
CONTAINER_NAME="echo-chamber-runner"
OUTPUT_FILE="echo_output.json"
DUMMY_CMD_SCRIPT="dummy_cmd.sh"

# Mock rationale: The dummy_cmd.sh script acts as a mock for any real-world command
# whose output and exit behavior we want to capture and replay. It provides
# deterministic output for testing the echo_chamber.sh's recording and replaying capabilities.
DUMMY_CMD_CONTENT='#!/bin/bash\necho "Hello from the past!"\nsleep 0.05 # Simulate some work\necho "Error from the void!" >&2\nexit 42\n'

# Cleanup function
cleanup() {
    echo "Cleaning up..."
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker rmi "$IMAGE_NAME" >/dev/null 2>&1 || true
    rm -f "$OUTPUT_FILE" "$DUMMY_CMD_SCRIPT" || true # Use || true to prevent script from failing if file doesn't exist
    rm -f Dockerfile.test || true
}

# Register cleanup on exit
trap cleanup EXIT

echo "--- Building Docker image ---"
# Create a temporary Dockerfile for testing, including the dummy command
cat <<EOF > Dockerfile.test
FROM alpine:latest

RUN apk add --no-cache bash jq

WORKDIR /app

COPY src/echo_chamber.sh /usr/local/bin/echo_chamber.sh
RUN chmod +x /usr/local/bin/echo_chamber.sh

COPY $DUMMY_CMD_SCRIPT /usr/local/bin/$DUMMY_CMD_SCRIPT
RUN chmod +x /usr/local/bin/$DUMMY_CMD_SCRIPT

ENTRYPOINT ["echo_chamber.sh"]
EOF

echo "$DUMMY_CMD_CONTENT" > "$DUMMY_CMD_SCRIPT"
chmod +x "$DUMMY_CMD_SCRIPT"

docker build -t "$IMAGE_NAME" -f Dockerfile.test .

echo "--- Test 1: Recording a command ---"
# Run the echo chamber in record mode
# We need to ensure the output file is written to the host, so mount a volume.
# The `docker run` command itself should exit with 0 if recording is successful.
docker run --name "$CONTAINER_NAME" -v "$(pwd):/app" "$IMAGE_NAME" record "/app/$OUTPUT_FILE" "$DUMMY_CMD_SCRIPT"
RECORD_EXIT_CODE=$?

if [[ "$RECORD_EXIT_CODE" -ne 0 ]]; then
    echo "FAIL: Recording command exited with non-zero code: $RECORD_EXIT_CODE"
    exit 1
fi

if [[ ! -f "$OUTPUT_FILE" ]]; then
    echo "FAIL: Output file $OUTPUT_FILE was not created."
    exit 1
fi

echo "--- Verifying recorded content ---"
# Verify the content of the recorded JSON
RECORDED_STDOUT=$(jq -r '.stdout' "$OUTPUT_FILE")
RECORDED_STDERR=$(jq -r '.stderr' "$OUTPUT_FILE")
RECORDED_EXIT_CODE=$(jq -r '.exit_code' "$OUTPUT_FILE")
RECORDED_DURATION=$(jq -r '.duration_seconds' "$OUTPUT_FILE")
RECORDED_COMMAND_ARRAY=$(jq -c '.command' "$OUTPUT_FILE") # Get the full command array as a JSON string

EXPECTED_STDOUT="Hello from the past!\n"
EXPECTED_STDERR="Error from the void!\n"
EXPECTED_EXIT_CODE="42"
EXPECTED_COMMAND_ARRAY='["/usr/local/bin/dummy_cmd.sh"]' # The command array should contain the dummy script

if [[ "$RECORDED_STDOUT" != "$EXPECTED_STDOUT" ]]; then
    echo "FAIL: Recorded stdout mismatch."
    echo "Expected: '$EXPECTED_STDOUT'"
    echo "Got:      '$RECORDED_STDOUT'"
    exit 1
fi

if [[ "$RECORDED_STDERR" != "$EXPECTED_STDERR" ]]; then
    echo "FAIL: Recorded stderr mismatch."
    echo "Expected: '$EXPECTED_STDERR'"
    echo "Got:      '$RECORDED_STDERR'"
    exit 1
fi

if [[ "$RECORDED_EXIT_CODE" != "$EXPECTED_EXIT_CODE" ]]; then
    echo "FAIL: Recorded exit code mismatch."
    echo "Expected: '$EXPECTED_EXIT_CODE'"
    echo "Got:      '$RECORDED_EXIT_CODE'"
    exit 1
fi

if (( $(echo "$RECORDED_DURATION <= 0" | bc -l) )); then
    echo "FAIL: Recorded duration should be positive."
    echo "Got: $RECORDED_DURATION"
    exit 1
fi

if [[ "$RECORDED_COMMAND_ARRAY" != "$EXPECTED_COMMAND_ARRAY" ]]; then
    echo "FAIL: Recorded command array mismatch."
    echo "Expected: '$EXPECTED_COMMAND_ARRAY'"
    echo "Got:      '$RECORDED_COMMAND_ARRAY'"
    exit 1
}

echo "Recorded content verified successfully."

echo "--- Test 2: Replaying the recorded command ---"
# Use temporary files to capture stdout and stderr from the docker run command
REPLAY_STDOUT_FILE=$(mktemp)
REPLAY_STDERR_FILE=$(mktemp)

# Run the echo chamber in replay mode
# The `docker run` command itself will exit with the replayed exit code.
docker run --rm -v "$(pwd):/app" "$IMAGE_NAME" replay "/app/$OUTPUT_FILE" > "$REPLAY_STDOUT_FILE" 2> "$REPLAY_STDERR_FILE"
REPLAY_EXIT_CODE=$?

REPLAY_STDOUT=$(cat "$REPLAY_STDOUT_FILE")
REPLAY_STDERR=$(cat "$REPLAY_STDERR_FILE")

rm "$REPLAY_STDOUT_FILE" "$REPLAY_STDERR_FILE"

if [[ "$REPLAY_STDOUT" != "$EXPECTED_STDOUT" ]]; then
    echo "FAIL: Replayed stdout mismatch."
    echo "Expected: '$EXPECTED_STDOUT'"
    echo "Got:      '$REPLAY_STDOUT'"
    exit 1
fi

# The replay script prints "Simulating temporal distortion..." and "Replay complete..." to stderr.
# We need to check if the *original* stderr content is present.
if ! echo "$REPLAY_STDERR" | grep -q "$EXPECTED_STDERR"; then
    echo "FAIL: Replayed stderr missing original content."
    echo "Expected to find: '$EXPECTED_STDERR'"
    echo "Got:              '$REPLAY_STDERR'"
    exit 1
fi

# Also check for the replay specific messages in stderr
if ! echo "$REPLAY_STDERR" | grep -q "Simulating temporal distortion:"; then
    echo "FAIL: Replay stderr missing 'Simulating temporal distortion:' message."
    exit 1
fi
if ! echo "$REPLAY_STDERR" | grep -q "Replay complete. Exiting with code $EXPECTED_EXIT_CODE."; then
    echo "FAIL: Replay stderr missing 'Replay complete.' message."
    exit 1
fi


if [[ "$REPLAY_EXIT_CODE" != "$EXPECTED_EXIT_CODE" ]]; then
    echo "FAIL: Replayed exit code mismatch."
    echo "Expected: '$EXPECTED_EXIT_CODE'"
    echo "Got:      '$REPLAY_EXIT_CODE'"
    exit 1
fi

echo "Replay verified successfully."

echo "All tests passed!"
