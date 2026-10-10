package main

import (
	"context"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
)

const (
	requestTimeout = 5 * time.Second
)

// NodeStatus holds the result of checking a node
type NodeStatus struct {
	URL        string
	Status     string
	Latency    time.Duration
	StatusCode int
	Error      error
}

// checkNode performs an HTTP GET request to the given URL and returns its status.
func checkNode(url string, results chan<- NodeStatus) {
	ctx, cancel := context.WithTimeout(context.Background(), requestTimeout)
	defer cancel()

	req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
	if err != nil {
		results <- NodeStatus{URL: url, Status: "Lost in the Static (Request Error)", Error: err}
		return
	}

	client := http.DefaultClient // Use default client, but with context timeout
	start := time.Now()
	resp, err := client.Do(req)
	latency := time.Since(start)

	status := NodeStatus{
		URL:     url,
		Latency: latency,
	}

	if err != nil {
		status.Error = err
		if strings.Contains(err.Error(), "context deadline exceeded") {
			status.Status = "Faint Echo (Timeout)"
		} else if strings.Contains(err.Error(), "connection refused") {
			status.Status = "Lost in the Static (Connection Refused)"
		} else if strings.Contains(err.Error(), "no such host") {
			status.Status = "Lost in the Static (Unknown Host)"
		} else {
			status.Status = "Lost in the Static (Network Error)"
		}
	} else {
		defer resp.Body.Close()
		status.StatusCode = resp.StatusCode
		if resp.StatusCode >= 200 && resp.StatusCode < 300 {
			status.Status = "Signal Strong"
			// Ensure body is read to properly close connection and reuse
			_, _ = io.Copy(io.Discard, resp.Body)
		} else if resp.StatusCode >= 400 && resp.StatusCode < 500 {
			status.Status = "Faint Echo (Client Error)"
		} else if resp.StatusCode >= 500 {
			status.Status = "Lost in the Static (Server Error)"
		} else {
			status.Status = "Whisper Detected (Unexpected Status)"
		}
	}
	results <- status
}

// run is the main logic function, separated for testing.
func run(args []string, stdout io.Writer) int {
	if len(args) < 1 {
		fmt.Fprintln(stdout, "Usage: nightly-whispernet-amplifier <URL1> [URL2]...")
		return 1
	}

	nodes := args
	results := make(chan NodeStatus, len(nodes))
	var wg sync.WaitGroup

	fmt.Fprintln(stdout, "--- WhisperNet Signal Amplifier Report ---")
	fmt.Fprintf(stdout, "Scanning %d critical nodes...\n\n", len(nodes))

	for _, nodeURL := range nodes {
		wg.Add(1)
		go func(url string) {
			defer wg.Done()
			checkNode(url, results)
		}(nodeURL)
	}

	wg.Wait()
	close(results)

	for res := range results {
		fmt.Fprintf(stdout, "Node: %s\n", res.URL)
		fmt.Fprintf(stdout, "  Status: %s", res.Status)
		if res.Error != nil {
			fmt.Fprintf(stdout, " (%v)", res.Error)
		}
		fmt.Fprintln(stdout)
		fmt.Fprintf(stdout, "  Latency: %s\n", res.Latency)
		if res.StatusCode != 0 {
			fmt.Fprintf(stdout, "  HTTP Code: %d\n", res.StatusCode)
		}
		fmt.Fprintln(stdout, "----------------------------------------")
	}

	fmt.Fprintln(stdout, "\n--- Scan Complete ---")
	return 0
}

func main() {
	// os.Args[0] is the program name, so pass os.Args[1:] to run
	exitCode := run(os.Args[1:], os.Stdout)
	os.Exit(exitCode)
}
