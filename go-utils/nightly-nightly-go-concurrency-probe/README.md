## nightly-go-concurrency-probe

A whimsical yet useful Go utility designed to probe network services and assess their ability to handle concurrent connections gracefully. In the post-apocalyptic world, knowing which services can withstand a sudden surge of users (or desperate survivors) is crucial.

### Philosophy

"Concurrency is the bedrock of resilience." This tool helps identify services that can scale under pressure, preventing bottlenecks when they matter most.

### Usage

```bash
go run main.go <host> <port> <num_connections> <duration_seconds>
```

*   `<host>`: The hostname or IP address of the service to probe.
*   `<port>`: The port number of the service.
*   `<num_connections>`: The number of concurrent connections to establish.
*   `<duration_seconds>`: The duration in seconds to maintain the connections.

### Example

To probe a web server at `survivor-net.local` on port `8080` with `100` concurrent connections for `30` seconds:

```bash
go run main.go survivor-net.local 8080 100 30
```

### Output

The utility will report the number of successful connections, failed connections, and any errors encountered during the probing process. A higher success rate indicates better concurrent handling.

### Installation

1.  Ensure you have Go installed.
2.  Clone this repository: `git clone https://github.com/polsala/ApocalypsAI.git`
3.  Navigate to the utility directory: `cd ApocalypsAI/go-utils/nightly-go-concurrency-probe/`
4.  Build the executable: `go build -o concurrency_probe`

### Testing

Run the tests using:

```bash
go test ./...
```
