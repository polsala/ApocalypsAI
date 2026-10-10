package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
)

// BeaconResult holds the status of a monitored beacon.
type BeaconResult struct {
	URL        string
	Status     string
	StatusCode int
	Latency    time.Duration
	Error      error
}

// checkBeacon performs an HTTP GET request to the given URL and sends the result to the channel.
func checkBeacon(url string, timeout time.Duration, results chan<- BeaconResult, wg *sync.WaitGroup) {
	defer wg.Done()

	start := time.Now()
	client := http.Client{
		Timeout: timeout,
	}

	resp, err := client.Get(url)
	latency := time.Since(start)

	if err != nil {
		// Check for specific error types to give more whimsical messages
		if os.IsTimeout(err) || strings.Contains(err.Error(), "timeout") || strings.Contains(err.Error(), "context deadline exceeded") {
			results <- BeaconResult{URL: url, Status: "lost its signal", Error: err, Latency: latency}
		} else if strings.Contains(err.Error(), "connection refused") || strings.Contains(err.Error(), "no such host") || strings.Contains(err.Error(), "dial tcp") {
			results <- BeaconResult{URL: url, Status: "faint and unreachable", Error: err, Latency: latency}
		} else {
			results <- BeaconResult{URL: url, Status: "struggling", Error: err, Latency: latency}
		}
		return
	}
	defer resp.Body.Close()

	// Read body to ensure connection is fully closed and latency includes this part
	_, _ = ioutil.ReadAll(resp.Body)

	if resp.StatusCode >= 200 && resp.StatusCode < 300 {
		results <- BeaconResult{URL: url, Status: "pulsing strongly", StatusCode: resp.StatusCode, Latency: latency}
	} else if resp.StatusCode >= 400 && resp.StatusCode < 500 {
		results <- BeaconResult{URL: url, Status: "emitting strange echoes", StatusCode: resp.StatusCode, Latency: latency}
	} else if resp.StatusCode >= 500 && resp.StatusCode < 600 {
		results <- BeaconResult{URL: url, Status: "experiencing temporal distortions", StatusCode: resp.StatusCode, Latency: latency}
	} else {
		results <- BeaconResult{URL: url, Status: "sending an unknown signal", StatusCode: resp.StatusCode, Latency: latency}
	}
}

// exit is a variable to allow mocking os.Exit in tests.
var exit = os.Exit

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run src/main.go <url1> <url2> ...")
		exit(1)
	}

	urls := os.Args[1:]
	results := make(chan BeaconResult, len(urls))
	var wg sync.WaitGroup

	const defaultTimeout = 5 * time.Second

	fmt.Println("\nInitiating Beacon Pulse Scan...")

	for _, url := range urls {
		wg.Add(1)
		go checkBeacon(url, defaultTimeout, results, &wg)
	}

	// Wait for all goroutines to finish, then close the results channel
	go func() {
		wg.Wait()
		close(results)
	}()

	// Collect and print results
	for res := range results {
		if res.Error != nil {
			fmt.Printf("Beacon %s %s (Error: %v, Latency: %s)\n", res.URL, res.Status, res.Error, res.Latency.Round(time.Millisecond))
		} else {
			fmt.Printf("Beacon %s %s (Status: %d, Latency: %s)\n", res.URL, res.Status, res.StatusCode, res.Latency.Round(time.Millisecond))
		}
	}

	fmt.Println("\nBeacon Pulse Scan Complete.")
}
