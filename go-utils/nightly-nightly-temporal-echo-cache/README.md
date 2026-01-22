# nightly-temporal-echo-cache

A whimsical-yet-useful Go-based ephemeral key-value cache that emits "temporal echoes" (notifications) when entries expire. Perfect for managing short-lived data, session states, or simulating memory decay in your distributed systems.

## Features

*   **Ephemeral Storage**: Store key-value pairs with a configurable Time-To-Live (TTL).
*   **Temporal Echoes**: When an entry expires, a "temporal echo" message is generated, indicating which key and value have faded into the past. These echoes can be retrieved for logging or further processing.
*   **Concurrent Safe**: Built with Go's concurrency primitives (`goroutines`, `channels`, `sync.Mutex`) for safe access from multiple routines.
*   **Simple API**: Easy to `Set`, `Get`, and `Delete` entries.
*   **Configurable Cleaner**: The background cleaner goroutine's interval can be configured.

## Usage

### Installation

To use this utility, you need Go installed (version 1.16 or higher recommended).

1.  Clone the repository (or navigate to the `go-utils/nightly-temporal-echo-cache` directory if already cloned).
2.  Run the main application:
    ```bash
    go run src/main.go
    ```

### Example

```go
package main

import (
	"fmt"
	"time"
)

// Assuming EchoCache and related structs/methods are in the same package or imported.
// For this example, we'll use the main package as defined in src/main.go

func main() {
	// Initialize the cache with a cleaner running every 500 milliseconds
	cache := NewEchoCache(500 * time.Millisecond)
	defer cache.StopCleaner() // Ensure the cleaner goroutine is stopped on exit

	fmt.Println("--- Setting entries ---")
	// Set a key "message" to expire in 2 seconds
	cache.Set("message", "Hello from the past!", 2)
	// Set another key "secret" to expire in 4 seconds
	cache.Set("secret", "42", 4)

	// Try to retrieve "message" immediately
	val, ok := cache.Get("message")
	if ok {
		fmt.Printf("Retrieved 'message': %s\n", val)
	} else {
		fmt.Println("'message' not found or expired.")
	}

	fmt.Println("\n--- Waiting for 'message' to expire (2.5 seconds) ---")
	time.Sleep(2500 * time.Millisecond) // Wait a bit longer than 'message' TTL

	// Try to retrieve "message" again (should be expired)
	val, ok = cache.Get("message")
	if ok {
		fmt.Printf("Retrieved 'message': %s\n", val)
	} else {
		fmt.Println("'message' not found or expired.")
	}

	// Check for temporal echoes
	echoes := cache.GetEchoes()
	if len(echoes) > 0 {
		fmt.Println("\n--- Temporal Echoes after 2.5s ---")
		for _, echo := range echoes {
			fmt.Println(echo)
		}
	} else {
		fmt.Println("\nNo temporal echoes yet.")
	}

	fmt.Println("\n--- Waiting for 'secret' to expire (another 2 seconds) ---")
	time.Sleep(2000 * time.Millisecond) // Wait for 'secret' to expire (total 4.5s)

	// Try to retrieve "secret" (should be expired)
	val, ok = cache.Get("secret")
	if ok {
		fmt.Printf("Retrieved 'secret': %s\n", val)
	} else {
		fmt.Println("'secret' not found or expired.")
	}

	// Check for new temporal echoes
	echoes = cache.GetEchoes()
	if len(echoes) > 0 {
		fmt.Println("\n--- Temporal Echoes after 4.5s ---")
		for _, echo := range echoes {
			fmt.Println(echo)
		}
	} else {
		fmt.Println("\nNo new temporal echoes.")
	}

	fmt.Println("\n--- Deleting an entry ---")
	cache.Set("temp_key", "temp_value", 10) // Set a key
	fmt.Printf("Before delete: %v\n", cache.Get("temp_key"))
	cache.Delete("temp_key") // Delete it
	fmt.Printf("After delete: %v\n", cache.Get("temp_key"))
}
```

## Development

### Running Tests

To run the tests, navigate to the utility's root directory and execute:

```bash
go test ./tests/...
```

The tests are designed to be deterministic and offline, using short `time.Sleep` calls to simulate time progression for expiration checks.

## Contributing

Feel free to contribute by opening issues or pull requests.

## License

This project is licensed under the MIT License.
