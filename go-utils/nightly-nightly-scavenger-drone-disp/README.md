# Nightly Scavenger Drone Dispatcher

The **Nightly Scavenger Drone Dispatcher** is a Go-based utility designed to simulate dispatching a fleet of "scavenger drones" to various "resource locations" (URLs). It concurrently fetches data from a list of provided URLs, reporting on the status, response time, and a snippet of the response body for each. This tool is useful for quickly checking the availability and basic content of multiple web endpoints or simulated data sources in a concurrent fashion.

## Features

*   **Concurrent Fetching**: Utilizes Go goroutines to fetch multiple URLs simultaneously.
*   **Status Reporting**: Provides HTTP status codes, response times, and error messages.
*   **Body Snippet**: Includes a small portion of the response body for quick content verification.
*   **Configurable Timeout**: Prevents drones from getting stuck indefinitely.

## Usage

### Prerequisites

*   Go (version 1.16 or higher)

### Build

```bash
cd go-utils/nightly-scavenger-drone-dispat
go build -o scavenger-dispatcher src/main.go
```

### Run

The dispatcher expects a list of URLs as command-line arguments.

```bash
./scavenger-dispatcher https://example.com https://httpbin.org/status/404 https://google.com
```

**Example Output:**

```
Dispatching 3 scavenger drones...
[DRONE 1] https://example.com - Status: 200 OK, Latency: 123.45ms, Body Snippet: "<!doctype html>\n<html>\n<head>\n    <title>Example Domain</title>"
[DRONE 2] https://httpbin.org/status/404 - Status: 404 Not Found, Latency: 56.78ms, Body Snippet: ""
[DRONE 3] https://google.com - Status: 200 OK, Latency: 234.56ms, Body Snippet: "<!doctype html><html itemscope=\"\" itemtype=\"http://schema.org/WebPage\" lang=\"en\">"
All scavenger drones have returned.
```

### Configuration (Optional)

You can modify the `defaultTimeout` and `bodySnippetLen` constants in `src/main.go` if needed.

## Development

### Running Tests

```bash
cd go-utils/nightly-scavenger-drone-dispat
go test ./tests/...
```
