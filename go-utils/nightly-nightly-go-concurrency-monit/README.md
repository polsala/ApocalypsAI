## Nightly Go Concurrency Monitor

This utility provides a simple yet effective way to monitor the number of active goroutines in a running Go application. It exposes this information via an HTTP endpoint, allowing for easy integration with monitoring dashboards or manual inspection.

### Philosophy

Inspired by the need for visibility into concurrent Go applications, this tool aims to be lightweight, easy to use, and provide actionable insights into goroutine activity.

### Features

*   Exposes goroutine count via an HTTP endpoint.
*   Minimal dependencies.
*   Easy to integrate into existing Go applications.

### Usage

1.  **Include the package:** Add the `concurrencymonitor` package to your Go project.
    ```bash
    go get github.com/polsala/ApocalypsAI/utils/nightly-go-concurrency-monitor/concurrencymonitor
    ```

2.  **Initialize and start the monitor:** In your application's `main` function or initialization phase, start the monitor.
    ```go
    package main

    import (
        "net/http"
        "log"
        "github.com/polsala/ApocalypsAI/utils/nightly-go-concurrency-monitor/concurrencymonitor"
    )

    func main() {
        // Start the concurrency monitor on port 8081
        go concurrencymonitor.Start(":8081")

        // Your application logic here...
        log.Println("Application started. Concurrency monitor running on :8081")

        // Keep the main goroutine alive (e.g., by starting an HTTP server for your app)
        http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
            w.Write([]byte("Hello from your app!"))
        })
        log.Fatal(http.ListenAndServe(":8080", nil))
    }
    ```

3.  **Access the metrics:** The monitor will expose metrics at `http://localhost:8081/metrics` (or the port you configured).
    You can use `curl` to fetch the data:
    ```bash
    curl http://localhost:8081/metrics
    ```

    The output will be in Prometheus exposition format, e.g.:
    ```
    # HELP go_goroutines_total Number of goroutines currently running.
    # TYPE go_goroutines_total gauge
    go_goroutines_total 15
    ```

### Testing

This utility includes unit tests that verify the functionality of the `Start` function and the metrics endpoint without requiring a live HTTP server.

### Contributing

Feel free to fork this repository and submit pull requests for new features or improvements.
