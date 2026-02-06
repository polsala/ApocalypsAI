# Go Concurrency Monitor

This utility provides a whimsical yet useful way to visualize the concurrency of your running Go applications. It leverages Go's built-in runtime metrics to offer insights into goroutine activity.

## Philosophy

"Anarchy with discipline" — this tool aims to provide visibility into the chaotic world of concurrent Go programs, offering a structured way to understand their behavior.

## Features

*   **Real-time Goroutine Count**: Displays the current number of active goroutines.
*   **Goroutine Lifecycle Visualization**: (Future enhancement) A simple visualization of goroutine states.
*   **Network Interface**: Exposes metrics over a simple HTTP endpoint for integration with other monitoring tools.

## Installation

1.  **Prerequisites**: Ensure you have Go installed (version 1.18 or later recommended).
2.  **Clone the repository**: `git clone https://github.com/polsala/ApocalypsAI.git`
3.  **Navigate to the utility**: `cd ApocalypsAI/utils/nightly-go-concurrency-monitor`
4.  **Build the utility**: `go build -o concurrency-monitor .`

## Usage

Run the compiled binary:

```bash
./concurrency-monitor
```

The monitor will start an HTTP server on `http://localhost:8080`. You can access the metrics by visiting this URL in your browser or using `curl`.

### Example: Monitoring a Sample Go App

Create a simple Go application that spawns a few goroutines:

```go
package main

import (
	"fmt"
	"net/http"
	"runtime"
	"time"
)

func worker(id int) {
	fmt.Printf("Worker %d started\n", id)
	ttime.Sleep(5 * time.Second)
	fmt.Printf("Worker %d finished\n", id)
}

func main() {
	// Start some worker goroutines
	for i := 0; i < 10; i++ {
		go worker(i)
	}

	// Keep the main goroutine alive
	select {}
}
```

Run this sample app. Then, run the `concurrency-monitor` in a separate terminal.

Access `http://localhost:8080` to see the current goroutine count.

## How it Works

This utility uses the `runtime.NumGoroutine()` function to get the current number of goroutines. It exposes this information via a simple HTTP server.

## Testing

Automated tests are included to ensure the core functionality works as expected. Run them using:

```bash
go test ./...
```
