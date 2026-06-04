# Nightly Go Concurrency Monitor

This utility provides a simple, yet effective, way to monitor and visualize the number of active goroutines in a running Go application. It exposes this information via an HTTP endpoint, allowing for easy integration with monitoring dashboards or simple inspection.

## Philosophy

Inspired by the need for visibility into concurrent systems, this tool aims to be lightweight and easy to integrate. It leverages Go's built-in runtime metrics to provide real-time insights without significant overhead.

## Features

*   Exposes goroutine count via an HTTP endpoint.
*   Minimal dependencies.
*   Easy to embed within existing Go applications.

## Usage

1.  **Import the package**: Add `"github.com/polsala/ApocalypsAI/utils/nightly-go-concurrency-monitor/src/monitor"` to your Go project.
2.  **Initialize the monitor**: Call `monitor.Start(":8080")` in your `main` function or an appropriate initialization point. This will start an HTTP server on the specified port.
3.  **Access the metrics**: Navigate to `http://localhost:8080/goroutines` in your browser or use `curl` to fetch the current goroutine count.

## Example Integration

```go
package main

import (
	"fmt"
	"net/http"
	"time"
	"github.com/polsala/ApocalypsAI/utils/nightly-go-concurrency-monitor/src/monitor"
)

func main() {
	// Start the concurrency monitor on port 8080
	go monitor.Start(":8080")

	// Simulate some work and goroutines
	for i := 0; i < 5; i++ {
		go func(id int) {
			fmt.Printf("Goroutine %d started\n", id)
			time.Sleep(5 * time.Second)
			fmt.Printf("Goroutine %d finished\n", id)
		}(i)
	}

	// Keep the main goroutine alive
	select {}
}
```

## Testing

Unit tests are included to verify the functionality of the monitor. Run them using `go test ./...` within the utility's directory.
