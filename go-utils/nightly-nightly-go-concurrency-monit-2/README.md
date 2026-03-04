## nightly-go-concurrency-monitor

A whimsical yet useful Go utility to peek under the hood of your concurrent Go applications. It provides insights into Goroutine activity and channel usage, helping you understand and optimize your concurrent code.

### Usage

1.  **Build:**
    ```bash
    go build -o concurrency_monitor ./src/main.go
    ```

2.  **Run:**
    The monitor needs to be integrated into your Go application. You can do this by:
    *   Importing the `monitor` package.
    *   Calling `monitor.Start()` at the beginning of your `main` function.
    *   Calling `monitor.Stop()` before your `main` function exits.

    The monitor will then expose an HTTP endpoint (defaulting to `:8080/metrics`) that provides the concurrency metrics.

    **Example Integration:**
    ```go
    package main

    import (
    	"fmt"
    	"net/http"
    	"time"

    	"github.com/polsala/ApocalypsAI/go-utils/nightly-go-concurrency-monitor/src/monitor"
    )

    func main() {
    	// Start the concurrency monitor
    	monitor.Start(nil) // Use default port 8080

    	fmt.Println("Application started. Concurrency metrics available at http://localhost:8080/metrics")

    	// Simulate some concurrent work
    	go func() {
    		for i := 0; i < 10; i++ {
    			time.Sleep(1 * time.Second)
    			fmt.Printf("Worker %d doing work\n", i)
    		}
    	}()

    	// Keep the main goroutine alive
    	select {}
    }
    ```

3.  **Access Metrics:**
    Once your application is running with the monitor integrated, you can access the metrics by navigating to `http://localhost:8080/metrics` in your browser or using `curl`:
    ```bash
    curl http://localhost:8080/metrics
    ```

### Metrics Exposed

*   `app_goroutines_total`: Total number of Goroutines currently running.
*   `app_goroutines_running`: Number of Goroutines in the `_running` state.
*   `app_goroutines_syscall`: Number of Goroutines in the `_syscall` state.
*   `app_goroutines_waiting`: Number of Goroutines in the `_waiting` state.
*   `app_channels_created_total`: Total number of channels created.
*   `app_channels_in_use_total`: Total number of channels currently in use.

### Contributing

Feel free to fork this repository and submit pull requests with improvements or new features!
