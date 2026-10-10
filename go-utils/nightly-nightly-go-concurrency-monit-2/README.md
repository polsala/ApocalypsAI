# Go Concurrency Monitor

This utility, built with Go, provides insights into the concurrent execution of Goroutines and the status of channels within a running Go program. It's designed to be a whimsical yet useful tool for understanding and debugging concurrency patterns in your applications.

## Philosophy

"Observe the dance of the Goroutines, lest they trip over each other in the digital void."

## Features

*   **Goroutine Count:** Reports the total number of active Goroutines.
*   **Channel Activity:** Tracks basic channel operations (send/receive) to give a sense of data flow.
*   **Goroutine Stack Traces (Optional):** Can be configured to capture stack traces for a deeper dive into Goroutine states.
*   **Whimsical Output:** Presents information with a touch of apocalyptic flair.

## Usage

1.  **Build:**
    ```bash
    go build -o concurrency-monitor .
    ```

2.  **Run:**
    The `concurrency-monitor` executable can be run as a standalone application. It will start a background monitoring service. To integrate it into your application, you would typically start it as a separate process or embed its logic.

    ```bash
    ./concurrency-monitor
    ```

    By default, it listens on `localhost:8080` for commands.

3.  **Interacting with the Monitor:**
    You can send commands to the monitor via HTTP requests to its API.

    *   **Get Status:**
        ```bash
        curl http://localhost:8080/status
        ```
        This will return a JSON object with the current Goroutine count and channel activity.

    *   **Enable Stack Traces:**
        ```bash
        curl http://localhost:8080/stacks/enable
        ```

    *   **Disable Stack Traces:**
        ```bash
        curl http://localhost:8080/stacks/disable
        ```

## Integration Example (Conceptual)

To monitor a specific Go application, you would typically run this monitor alongside your application and have your application expose metrics that the monitor can scrape, or have the monitor directly instrument your application's Goroutines and channels (which is more complex and often done via libraries).

For this standalone utility, imagine it's monitoring a hypothetical set of background tasks.

## Testing

Run tests using `go test ./...`.

## License

This project is licensed under the MIT License.
