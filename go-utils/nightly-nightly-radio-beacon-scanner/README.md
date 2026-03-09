# Radio Beacon Scanner

A whimsical yet practical Go CLI that concurrently scans a list of hosts for a custom beacon string (e.g., "SURVIVE"). Useful for post‑apocalyptic scenarios where you need to locate active radio stations or services.

## Install

```sh
go build -o beacon-scanner ./src/main.go
```

## Usage

```sh
./beacon-scanner -hosts hosts.txt -port 8080 -keyword SURVIVE -timeout 2s
```

- `-hosts`   : path to a file containing one hostname per line.
- `-port`    : TCP port to connect to on each host.
- `-keyword` : beacon string to look for in the response.
- `-timeout` : connection timeout (default 2s).

The tool prints each host followed by `FOUND` or `NOT FOUND`.

## How it works

- Reads the host list.
- Launches up to 100 concurrent workers.
- For each host, opens a TCP connection, sends a simple HTTP GET request, reads up to 1 KB of response, and checks for the keyword.
- Reports results.
