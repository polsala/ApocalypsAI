## Nightly Go Concurrency Monitor

This utility provides a simple, yet effective, way to monitor and visualize the concurrency of running Go processes on your system. It leverages Go's built-in runtime metrics to provide insights into goroutine activity.

### Features

*   Lists all running Go processes.
*   For each process, displays the number of active goroutines.
*   Provides a basic visualization of goroutine counts over time.

### Usage

1.  **Build the utility:**
    ```bash
    go build -o concurrency-monitor ./src/main.go
    ```

2.  **Run the utility:**
    ```bash
    ./concurrency-monitor
    ```

    The utility will start and display a live-updating table of Go processes and their goroutine counts. Press `Ctrl+C` to exit.

### How it Works

The `concurrency-monitor` executable finds running Go processes by inspecting the `/proc` filesystem (on Linux-like systems). For each Go process, it attaches to its runtime and queries the `runtime.NumGoroutine()` metric. This data is then displayed in a table and can be optionally visualized (though the current implementation focuses on the table display for simplicity and offline testability).

### Testing

Automated tests are included to ensure the core logic functions correctly. These tests mock the process inspection and goroutine count retrieval to provide deterministic and offline execution.

```bash
cd tests
go test
```
