## nightly-go-concurrent-ping

A whimsical yet useful Go utility that concurrently pings a list of hosts and reports their status. It's designed to be fast and efficient, leveraging Go's concurrency features to check multiple targets simultaneously.

### Philosophy

In the face of digital chaos, knowing which nodes are still responsive is crucial. This tool provides a quick, concurrent way to check the pulse of your network, even if the network itself is a bit... wobbly.

### Usage

1. **Build the utility:**
   ```bash
   go build -o concurrent-ping main.go
   ```

2. **Run the utility:**
   The utility accepts a comma-separated list of hostnames or IP addresses as a command-line argument.
   ```bash
   ./concurrent-ping google.com,8.8.8.8,invalid.host,1.1.1.1
   ```

### Output

The utility will output the status of each host (e.g., 'UP', 'DOWN', 'ERROR') along with the time taken for the ping.

```
Host: google.com, Status: UP, Time: 25ms
Host: 8.8.8.8, Status: UP, Time: 30ms
Host: invalid.host, Status: ERROR, Error: lookup invalid.host: no such host
Host: 1.1.1.1, Status: UP, Time: 28ms
```

### Testing

Run the tests using:
```bash
go test -v ./...
```

### Contributing

This is a community utility. Feel free to fork, improve, and submit pull requests!
