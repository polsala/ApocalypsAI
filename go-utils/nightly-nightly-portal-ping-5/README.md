# nightly-portal-ping

A whimsical concurrent port scanner that discovers open ports on a host and celebrates each find with a fun emoji. It runs fast by scanning multiple ports in parallel.

## Build

```sh
go build -o portal-ping ./src
```

## Usage

```sh
./portal-ping -host example.com -start 1 -end 1024 -workers 100
```

Will output lines like:

```
🔓 Port 22 is open! 🎉
```

## How it works

- Uses goroutines and a worker pool.
- Each worker attempts to `net.DialTimeout` with a 200 ms timeout.
- Results are collected, sorted, and printed with whimsical emojis.

## Testing

```sh
go test ./tests
```
