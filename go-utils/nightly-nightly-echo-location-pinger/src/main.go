package main

import (
	"fmt"
	"net"
	"os"
	"strings"
	"sync"
	"time"
)

// PingResult stores the outcome of a single ping operation.
type PingResult struct {
	Target  string
	Status  string // "Success", "Failed"
	Latency time.Duration
	Error   string
}

// dialer is a variable that holds the net.DialTimeout function.
// It's made a variable for easier mocking in tests.
var dialer = net.DialTimeout

// pingTarget attempts to establish a TCP connection to the given target.
func pingTarget(target string, timeout time.Duration) PingResult {
	start := time.Now()
	conn, err := dialer("tcp", target, timeout)
	duration := time.Since(start)

	if err != nil {
		return PingResult{Target: target, Status: "Failed", Latency: duration, Error: err.Error()}
	}
	defer conn.Close()
	return PingResult{Target: target, Status: "Success", Latency: duration, Error: ""}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: nightly-echo-location-pinger <target1> [target2...] [--timeout=<duration>]")
		fmt.Println("Example: nightly-echo-location-pinger google.com:80 192.168.1.1:22 --timeout=500ms")
		os.Exit(1)
	}

	targets := []string{}
	timeout := 5 * time.Second // Default timeout

	// Parse arguments for targets and timeout
	for _, arg := range os.Args[1:] {
		if strings.HasPrefix(arg, "--timeout=") {
			durationStr := strings.TrimPrefix(arg, "--timeout=")
			parsedTimeout, err := time.ParseDuration(durationStr)
			if err != nil {
				fmt.Printf("Error parsing timeout duration '%s': %v\n", durationStr, err)
				os.Exit(1)
			}
			timeout = parsedTimeout
		} else {
			targets = append(targets, arg)
		}
	}

	if len(targets) == 0 {
		fmt.Println("No targets specified. Usage: nightly-echo-location-pinger <target1> [target2...] [--timeout=<duration>]")
		os.Exit(1)
	}

	var wg sync.WaitGroup
	results := make(chan PingResult, len(targets))

	for _, target := range targets {
		wg.Add(1)
		go func(t string) {
			defer wg.Done()
			results <- pingTarget(t, timeout)
		}(target)
	}

	wg.Wait()
	close(results)

	fmt.Println("--- Echo-Location Report ---")
	// Collect results from the channel and print them
	// Note: The order of results might not match the input order due to concurrency.
	// For a sorted output, one would collect all results into a slice and then sort.
	for result := range results {
		if result.Status == "Success" {
			fmt.Printf("Target: %-25s Status: %-8s Latency: %s\n", result.Target, result.Status, result.Latency)
		} else {
			fmt.Printf("Target: %-25s Status: %-8s Error: %s\n", result.Target, result.Status, result.Error)
		}
	}
	fmt.Println("--------------------------")
}
