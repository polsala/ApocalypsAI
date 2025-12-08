# nightly-docker-emoji-log-printer

A whimsical yet useful Docker utility that reads a plain‑text log file (mounted at `/logs/input.log`) and prints each line prefixed with an emoji that reflects the log level.

## Features

- **Zero‑dependency**: Built on Alpine Linux with a tiny Bash script.
- **Emoji mapping**
  - `INFO` → ℹ️
  - `WARN` → ⚠️
  - `ERROR` → ❌
  - any other line → 🐞
- **Mount‑your‑logs**: Simply mount a directory containing `input.log` and run the container.

## Build the image

```bash
docker build -t emoji-log-printer .
```

## Run the container

```bash
# Assuming you have a directory "mylogs" with a file "input.log"
mkdir -p mylogs
cat > mylogs/input.log <<'EOF'
INFO Application started
WARN Low memory
ERROR Unexpected crash
DEBUG Some debug info
EOF

docker run --rm -v $(pwd)/mylogs:/logs emoji-log-printer
```

The output will be:

```
ℹ️ INFO Application started
⚠️ WARN Low memory
❌ ERROR Unexpected crash
🐞 DEBUG Some debug info
```

## How it works

The Docker image copies a tiny Bash script (`entrypoint.sh`) into the container. When the container starts, the script reads `/logs/input.log` line‑by‑line, matches the log level, and prints the appropriate emoji.

## Testing

Run the provided test script to verify the Dockerfile and entrypoint logic:

```bash
bash tests/test_dockerfile.sh
```

The tests are deterministic and do not require a running Docker daemon.
