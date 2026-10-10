# nightly-concurrent-ping-sweeper

A whimsical CLI tool that concurrently checks a list of hostnames (or IPs) for TCP reachability on port 80, reporting which ones are alive. Useful for quick network sanity checks in a post‑apocalyptic bunker.

## Installation

```sh
go build -o ping-sweeper ./src/main.go
```

## Usage

```sh
# Provide hosts as arguments
./ping-sweeper example.com google.com

# Or pipe a list via stdin
cat hosts.txt | ./ping-sweeper
```

## Options

- `-c N` – maximum concurrent checks (default 10)
- `-t ms` – timeout per connection in milliseconds (default 500)

## How it works

The tool spawns up to N goroutines, each attempting a TCP dial to port 80 with the specified timeout. Results are collected and printed.
