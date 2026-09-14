# Go Concurrency Monitor (nightly-go-concurrency-monitor)

This utility provides a simple, yet effective, way to monitor and visualize the goroutines within a running Go application. It exposes a web endpoint that displays a live count of active goroutines and their states, helping developers understand and debug concurrency issues.

## Philosophy

Inspired by the "anarchy with discipline" ethos, this tool leverages Go's built-in concurrency primitives and standard library to offer a lightweight, standalone solution. It aims to be useful without introducing heavy dependencies or complex configurations.

## Features

*   **Real-time Goroutine Count**: Displays the total number of active goroutines.
*   **Goroutine State Breakdown**: Shows counts for goroutines in different states (running, waiting, etc.).
*   **Lightweight Web Interface**: Accessible via a simple HTTP server.
*   **Self-Contained**: No external dependencies beyond the Go standard library.

## Usage

1.  **Integrate into your Go application**: Import the `concurrencymonitor` package into your project.
2.  **Start the monitor**: Call `concurrencymonitor.StartMonitor()` in your `main` function or an appropriate initialization point.
3.  **Access the dashboard**: Open your web browser to `http://localhost:8080/monitor` (or the configured address).

### Example Integration

```go
package main

import (
	"fmt"
	"net/http"
	"time"
	"github.com/polsala/ApocalypsAI/utils/nightly-go-concurrency-monitor/src/concurrencymonitor"
)

func main() {
	// Start the concurrency monitor on port 8080
	go concurrencymonitor.StartMonitor(":8080")

	// Your application logic here...
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Hello from the main app!")
	})

	fmt.Println("Main app started. Monitor available at http://localhost:8080/monitor")
	http.ListenAndServe(":3000", nil)
}
```

## Development & Testing

This utility is built with Go. To run the tests:

```bash
cd utils/nightly-go-concurrency-monitor
go test ./...
```

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
