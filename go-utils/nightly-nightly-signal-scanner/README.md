# Nightly Signal Scanner

A whimsical concurrent network scanner that treats each `host:port` as a radio frequency and reports whether a "signal" is received.

## Overview

- Reads a list of `host:port` entries from **STDIN** (one per line).
- Checks each address concurrently (default up to 10 at a time).
- Prints a friendly line indicating success or failure.

## Installation

```bash
# Build the binary (requires Go 1.22+)
go build -o signal-scanner ./src/main.go
```

## Usage

```bash
# Example input (you can pipe from a file, echo, etc.)
echo -e "example.com:80\nlocalhost:22" | ./signal-scanner -t 3
```

### Flags

- `-t int`   Connection timeout in seconds (default **2**).
- `-c int`   Maximum concurrent checks (default **10**).

## Output

For each input line the tool prints one of:

- `Signal received from <host:port>` – the TCP connection succeeded.
- `No signal from <host:port>` – the connection failed or timed out.

## Why "Signal"?

In a post‑apocalyptic world, every open port is a faint radio transmission. This utility helps you tune in to the ones that are still alive.
