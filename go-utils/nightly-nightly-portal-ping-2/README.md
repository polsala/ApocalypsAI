# nightly-portal-ping

A whimsical concurrent TCP latency checker that pings multiple hosts at once and reports the roundâtrip time. Perfect for explorers navigating the digital portals of the apocalypse.

## Build

```bash
go build -o portal-ping ./src/main.go
```

## Usage

```bash
./portal-ping host1.com host2.org ...
```

The tool attempts a TCP connection to port 80 (or the port specified with `host:port`) for each host, measures how long the connection takes, and prints the results in a table.

## Example

```bash
$ ./portal-ping example.com google.com:443
âââââââââââââââââ¬ââââââââââââââââ
â Host          â Latency (ms)  â
âââââââââââââââââ¼ââââââââââââââââ¤
â example.com   â 23            â
â google.com:443â 12            â
âââââââââââââââââ´ââââââââââââââââ
```

## Testing

Run the unit tests with:

```bash
go test ./... 
```
