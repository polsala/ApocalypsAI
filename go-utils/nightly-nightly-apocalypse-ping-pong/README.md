# Apocalypse Ping Pong

A whimsical concurrent TCP ping utility that checks a list of hosts and assigns a survival rating.

## Features

- Concurrent checks using goroutines.
- Simple rating: **Safe** for reachable hosts, **Dangerous** for unreachable.
- No external dependencies.

## Installation

```sh
go build -o pingpong ./src/main.go
```

## Usage

```sh
./pingpong example.com google.com
```

Output example:

```
example.com: reachable (Safe)
google.com: reachable (Safe)
nonexistent.tld: unreachable (Dangerous)
```

## How it works

The program attempts a TCP connection to port 80 of each host with a 2‑second timeout. Results are printed with a playful rating.

## Testing

Run the tests with:

```sh
go test ./tests
```
