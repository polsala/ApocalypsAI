# nightly-container-survival-kit

A minimal Docker image packed with essential tools for debugging, recovery, and diagnostics in restricted or emergency environments.

## Features

- Lightweight Alpine-based image
- Pre-installed tools: `curl`, `wget`, `ping`, `nslookup`, `dig`, `tcpdump`, `strace`, `htop`, `vim`
- Designed for ephemeral debugging sessions

## Usage

```bash
# Run interactively
docker run -it ghcr.io/polsala/nightly-container-survival-kit:latest

# Run a specific command
docker run --rm ghcr.io/polsala/nightly-container-survival-kit:latest curl -I https://example.com
```

## Build locally

```bash
docker build -t survival-kit .
```

## License
MIT
