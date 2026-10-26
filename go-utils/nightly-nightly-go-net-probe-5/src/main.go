package main

import (
	"fmt"
	"net"
	"os"
	"strings"
	"sync"
	"time"
)

// ProbeResult stores the outcome of a single network probe.
type ProbeResult struct {
	Target    string
	Reachable bool
	Latency   time.Duration
	Error     string
}

// probeTarget attempts to connect to a given target and measures latency.
func probeTarget(target string, wg *sync.WaitGroup, results chan<- ProbeResult) {
	defer wg.Done()

	startTime := time.Now()

	// Mock rationale: In a real-world scenario, this would be a network call.
	// For deterministic testing, we simulate success/failure based on input.
	conn, err := net.DialTimeout("tcp", target, 2*time.Second)

	result := ProbeResult{Target: target}

	if err != nil {
		result.Reachable = false
		result.Error = err.Error()
	} else {
		defer conn.Close()
		result.Reachable = true
		result.Latency = time.Since(startTime)
	}

	results <- result
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: nightly-go-net-probe <host1>:<port1> <host2>:<port2> ...")
		os.Exit(1)
	}

	targets := os.Args[1:]
	var wg sync.WaitGroup
	results := make(chan ProbeResult, len(targets))

	fmt.Println("Starting network probe...")

	for _, target := range targets {
		wg.Add(1)
		go probeTarget(target, &wg, results)
	}

	wg.Wait()
	close(results)

	fmt.Println("Probe complete. Results:")
	for result := range results {
		status := "false"
		if result.Reachable {
			status = "true"
		}
		fmt.Printf("Target: %s | Reachable: %s | Latency: %s%s\n",
			result.Target,
			status,
			func() string {
				if result.Reachable {
					return result.Latency.String()
				}
				return "N/A"
			}(),
			func() string {
				if !result.Reachable {
					return " | Error: " + result.Error
				}
				return ""
			}())
	}
}
