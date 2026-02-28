# Portal Ping
A concurrent port scanner that checks a range of ports on a host and reports which ports are open, sprinkling each result with a whimsical message.

## Build

```sh
go build -o portal-ping ./src
```

## Usage

```sh
./portal-ping -host example.com -start 80 -end 85
```

Outputs lines like:

```
🔓 Port 80 is open! The gate swings wide.
❌ Port 81 is closed. The gate remains shut.
...
```

## How it works

Uses goroutines and a worker pool to scan ports concurrently. The core scanning logic is testable via dependency injection of a dial function.
