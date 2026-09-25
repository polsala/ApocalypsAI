# Go Concurrency Monitor

This utility provides a simple yet effective way to monitor and visualize the number of active goroutines in a running Go application. It exposes an HTTP endpoint that can be scraped by monitoring systems or accessed directly for a quick overview.

## Features

*   Exposes goroutine count via an HTTP endpoint.
*   Lightweight and easy to integrate.
*   Provides a basic visualization of goroutine activity.

## Installation

This is a Go module. To use it, you'll need to have Go installed.

1.  Clone the repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/utils/nightly-go-concurrency-monitor
    ```

2.  Build the executable:
    ```bash
    go build -o concurrency-monitor .
    ```

## Usage

Run the compiled executable. By default, it will start an HTTP server on port 8080.

```bash
./concurrency-monitor
```

Once running, you can access the monitoring endpoint at `http://localhost:8080/metrics`.

## Integration

To integrate this into your existing Go application, you can embed the `goroutineMonitor` struct.

```go
package main

import (
	"net/http"
	"time"

	"github.com/polsala/ApocalypsAI/utils/nightly-go-concurrency-monitor/internal/monitor"
)

func main() {
	// Start the goroutine monitor in a separate goroutine
	go monitor.StartMonitor(8080) // Listen on port 8080

	// Your application logic here...
	// For demonstration, we'll just keep the main goroutine alive
	select {}
}
```

## Metrics Endpoint (`/metrics`)

This endpoint returns a plain text output with the current number of goroutines.

Example output:

```
# HELP go_goroutines_total The total number of goroutines.
# TYPE go_goroutines_total gauge
go_goroutines_total 15
```

## License

This project is licensed under the MIT License.
