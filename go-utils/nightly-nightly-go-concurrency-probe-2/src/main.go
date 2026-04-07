package main

import (
	"flag"
	"fmt"
	"net"
	"os"
	"strings"
	"sync"
	"time"
)

// ProbeResult represents the outcome of a service probe.
type ProbeResult struct {
	Target string
	IsUp   bool
	Error  error
}

// probeService attempts to connect to a given target (host:port).
// It returns a ProbeResult indicating success or failure.
func probeService(target string, timeout time.Duration, results chan<- ProbeResult, wg *sync.WaitGroup) {
	defer wg.Done()

	dialer := net.Dialer{Timeout: timeout}
	conn, err := dialer.Dial("tcp", target)

	result := ProbeResult{Target: target}
	if err != nil {
		result.IsUp = false
		result.Error = err
	} else {
		result.IsUp = true
		conn.Close() // Close the connection immediately after successful dial
	}

	results <- result
}

func main() {
	timeout := flag.Duration("timeout", 5*time.Second, "Timeout for each probe in seconds")
	flag.Parse()

	targets := flag.Args()

	if len(targets) == 0 {
		fmt.Println("Usage: concurrency_probe [-timeout duration] <host:port>...")
		os.Exit(1)
	}

	var wg sync.WaitGroup
	results := make(chan ProbeResult, len(targets))

	fmt.Printf("Probing %d services with a timeout of %s...\n", len(targets), *timeout)

	for _, target := range targets {
		// Basic validation for host:port format
		if !strings.Contains(target, ":") {
			fmt.Fprintf(os.Stderr, "Skipping invalid target format: %s (expected host:port)\n", target)
			continue
		}
		wg.Add(1)
		go probeService(target, *timeout, results, &wg)
	}

	wg.Wait()
	close(results)

	fmt.Println("\n--- Probe Results ---")
	upCount := 0
	downCount := 0

	for result := range results {
		if result.IsUp {
			fmt.Printf("[UP] %s\n", result.Target)
			upCount++
		} else {
			fmt.Printf("[DOWN] %s - Error: %v\n", result.Target, result.Error)
			downCount++
		}
	}

	fmt.Printf("\nSummary: %d services UP, %d services DOWN\n", upCount, downCount)
}
