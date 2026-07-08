package main

import (
	"fmt"
	"net/http"
	"os"
	"sync"
	"time"
)

// ProbeResult holds the outcome of a single probe.
type ProbeResult struct {
	Target  string
	Status  string
	Latency time.Duration
	Error   error
}

// probeTarget performs a single network probe.
func probeTarget(target string, wg *sync.WaitGroup, results chan<- ProbeResult) {
	defer wg.Done()

	startTime := time.Now()

	// Attempt to create an HTTP client with a timeout.
	client := &http.Client{
		Timeout: 5 * time.Second, // 5-second timeout for each probe
	}

	resp, err := client.Get(target)
	latency := time.Since(startTime)

	if err != nil {
		results <- ProbeResult{Target: target, Status: "Error", Latency: latency, Error: err}
		return
	}

	defer resp.Body.Close()

	// Basic check for HTTP status codes
	if resp.StatusCode >= 200 && resp.StatusCode < 300 {
		results <- ProbeResult{Target: target, Status: "OK", Latency: latency, Error: nil}
	} else {
		results <- ProbeResult{Target: target, Status: fmt.Sprintf("HTTP %d", resp.StatusCode), Latency: latency, Error: fmt.Errorf("unexpected status code: %d", resp.StatusCode)}
	}
}

func main() {
	var targets []string

	// Read targets from command line arguments or stdin
	if len(os.Args) > 1 {
		targets = os.Args[1:]
	} else {
		// Read from stdin if no arguments are provided
		scanner := bufio.NewScanner(os.Stdin)
		for scanner.Scan() {
			targets = append(targets, scanner.Text())
		}
		if err := scanner.Err(); err != nil {
			fmt.Fprintf(os.Stderr, "Error reading from stdin: %v\n", err)
			os.Exit(1)
		}
	}

	if len(targets) == 0 {
		fmt.Println("No targets provided. Please provide URLs as arguments or via stdin.")
		os.Exit(0)
	}

	var wg sync.WaitGroup
	results := make(chan ProbeResult, len(targets))

	fmt.Println("Starting network probes...")

	// Launch goroutines for each target
	for _, target := range targets {
		wg.Add(1)
		go probeTarget(target, &wg, results)
	}

	// Wait for all probes to complete
	wg.Wait()
	close(results)

	fmt.Println("\n--- Probe Results ---")
	// Process and print results
	for result := range results {
		if result.Error != nil {
			fmt.Printf("Target: %s, Status: %s, Latency: %s, Error: %v\n", result.Target, result.Status, result.Latency, result.Error)
		} else {
			fmt.Printf("Target: %s, Status: %s, Latency: %s\n", result.Target, result.Status, result.Latency)
		}
	}
	fmt.Println("---------------------")
}

// Mock rationale: bufio is a standard library package, no need to mock for basic functionality. 
// The core logic relies on net/http and time, which are tested via mocks in the tests/ directory.
