# Go Concurrency Monitor

This utility provides a simple yet effective way to monitor Goroutine activity and channel usage within a Go application. It's designed to be a lightweight tool that can be integrated into your existing Go projects to gain insights into concurrent operations.

## Features

*   **Goroutine Count**: Tracks the total number of active Goroutines.
*   **Channel Activity**: Monitors the number of Goroutines blocked on channel operations (send/receive).
*   **Runtime Metrics**: Exposes basic Go runtime statistics.

## Usage

1.  **Import the package**: Add `"github.com/polsala/ApocalypsAI/utils/nightly-go-concurrency-monitor/src/concurrency_monitor"` to your project.
2.  **Initialize the monitor**: Call `concurrency_monitor.Start()` early in your `main` function.
3.  **Access metrics**: The monitor exposes metrics via a simple HTTP endpoint (defaulting to `:8080/metrics`). You can customize the port.

```go
package main

import (
	"fmt"
	"net/http"
	"time"

	"github.com/polsala/ApocalypsAI/utils/nightly-go-concurrency-monitor/src/concurrency_monitor"
)

func main() {
	// Start the concurrency monitor on port 8080
	concurrency_monitor.Start(concurrency_monitor.WithPort(8080))

	// Simulate some work with Goroutines
	for i := 0; i < 5; i++ {
		go func(id int) {
			fmt.Printf("Goroutine %d started\n", id)
			time.Sleep(5 * time.Second)
			fmt.Printf("Goroutine %d finished\n", id)
		}(i)
	}

	// Simulate channel blocking
	ch := make(chan int)
	go func() {
		<-ch // This Goroutine will block here until a value is sent
		fmt.Println("Received from channel")
	}()

	// Keep the main Goroutine alive to allow others to run
	select {}
}
```

## Metrics Endpoint

By default, metrics are available at `http://localhost:8080/metrics`.

Example output:

```
# HELP go_goroutines_total The total number of Goroutines.
# TYPE go_goroutines_total gauge
go_goroutines_total 10
# HELP go_channel_blocked_goroutines The number of Goroutines blocked on channel operations.
# TYPE go_channel_blocked_goroutines gauge
go_channel_blocked_goroutines 1
```

## Configuration Options

Use `concurrency_monitor.Option` functions to customize the monitor:

*   `concurrency_monitor.WithPort(port int)`: Sets the HTTP port for the metrics endpoint.
*   `concurrency_monitor.WithInterval(interval time.Duration)`: Sets the interval for collecting and reporting metrics.

## Testing

Unit tests are included to verify the functionality of the monitor. They use mocks to simulate runtime behavior without requiring actual Go runtime interactions.
