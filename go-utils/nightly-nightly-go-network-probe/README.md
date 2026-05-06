# nightly-go-network-probe

A whimsical yet useful Go utility for concurrently probing network services. It checks for service availability and measures latency, providing a quick overview of your network's health.

## Philosophy

Inspired by the need for a simple, fast, and concurrent way to check if services are up and responsive, especially in a post-apocalyptic scenario where reliable communication is key. Built with Go for its excellent concurrency primitives and performance.

## Usage

Compile the Go program and run it with a list of target hosts and ports.

```bash
# Example:
./nightly-go-network-probe google.com:80 example.com:443 1.1.1.1:53
```

The output will show the status (UP/DOWN) and latency for each probed service.

## How it Works

The utility takes host:port combinations as command-line arguments. For each target, it launches a goroutine to perform a TCP connection attempt. It measures the time taken for the connection to establish or fail, reporting the result and latency.

## Testing

Tests are included to ensure the functionality of the probe. They use mocked network responses to provide deterministic and offline testing.

## Contributing

Feel free to fork this repository and submit pull requests with improvements or new features. All contributions are welcome!
