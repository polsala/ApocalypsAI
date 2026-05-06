package main

import (
	"fmt"
	"net"
	"os"
	"sync"
	"time"
)

// ProbeResult holds the outcome of a network probe.
type ProbeResult struct {
	Target  string
	Status  string
	Latency time.Duration
	Error   error
}

// probeTarget attempts to connect to a given host:port and measures latency.
func probeTarget(target string, wg *sync.WaitGroup, results chan<- ProbeResult) {
	defer wg.Done()

	start := time.Now()
	conn, err := net.DialTimeout("tcp", target, 5*time.Second) // 5-second timeout

	latency := time.Since(start)

	result := ProbeResult{Target: target}

	if err != nil {
		result.Status = "DOWN"
		result.Error = err
	} else {
		result.Status = "UP"
		result.Latency = latency
		conn.Close() // Close the connection immediately after successful probe
	}

	results <- result
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: nightly-go-network-probe <host:port> [<host:port> ...]")
		os.Exit(1)
	}

	targets := os.Args[1:]
	var wg sync.WaitGroup
	results := make(chan ProbeResult, len(targets))

	fmt.Println("Starting network probes...")

	for _, target := range targets {
		wg.Add(1)
		go probeTarget(target, &wg, results)
	}

	wg.Wait()
	close(results)

	fmt.Println("\n--- Probe Results ---")
	for result := range results {
		if result.Status == "UP" {
			fmt.Printf("%s: %s (Latency: %s)\n", result.Target, result.Status, result.Latency.Round(time.Millisecond))
		} else {
			fmt.Printf("%s: %s (Error: %v)\n", result.Target, result.Status, result.Error)
		}
	}
	fmt.Println("---------------------")
}
