package main

import (
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
)

type PingResult struct {
	Target  string
	Latency time.Duration
	Error   error
}

type TargetStats struct {
	MinLatency time.Duration
	MaxLatency time.Duration
	AvgLatency time.Duration
	Successes  int
	Failures   int
	Errors     []error
}

// pingTarget performs a single HTTP GET request to the given URL and measures latency.
// It sends the result to the provided channel.
func pingTarget(target string, timeout time.Duration, results chan<- PingResult) {
	start := time.Now()
	client := http.Client{
		Timeout: timeout,
	}

	resp, err := client.Get(target)
	latency := time.Since(start)

	if err != nil {
		results <- PingResult{Target: target, Latency: latency, Error: err}
		return
	}
	defer resp.Body.Close()

	// Read body to ensure full response is received and measured
	_, readErr := io.Copy(io.Discard, resp.Body)
	if readErr != nil {
		results <- PingResult{Target: target, Latency: latency, Error: readErr}
		return
	}

	results <- PingResult{Target: target, Latency: latency, Error: nil}
}

// runPings orchestrates concurrent pings for a single target.
func runPings(target string, count int, timeout time.Duration, results chan<- PingResult, wg *sync.WaitGroup) {
	defer wg.Done()
	for i := 0; i < count; i++ {
		pingTarget(target, timeout, results)
	}
}

// printStats outputs the collected ping statistics for a target.
func printStats(target string, stats TargetStats) {
	fmt.Printf("\n--- Ping Statistics for %s ---\n", target)
	fmt.Printf("  Pings Sent: %d\n", stats.Successes+stats.Failures)
	fmt.Printf("  Successful: %d\n", stats.Successes)
	fmt.Printf("  Failed: %d\n", stats.Failures)

	if stats.Successes > 0 {
		fmt.Printf("  Min Latency: %s\n", stats.MinLatency)
		fmt.Printf("  Max Latency: %s\n", stats.MaxLatency)
		fmt.Printf("  Avg Latency: %s\n", stats.AvgLatency)
	}

	if stats.Failures > 0 {
		fmt.Println("  Errors: ")
		for _, err := range stats.Errors {
			fmt.Printf("    %v\n", err)
		}
	}
}

func main() {
	// Define command-line flags
	targetsStr := flag.String("targets", "", "Comma-separated list of URLs/IPs to ping")
	count := flag.Int("count", 1, "Number of times to ping each target")
	timeoutStr := flag.String("timeout", "3s", "Timeout for each ping (e.g., 1s, 500ms)")
	flag.Parse()

	if *targetsStr == "" {
		fmt.Println("Error: -targets flag is required.")
		flag.Usage()
		os.Exit(1)
	}

	timeout, err := time.ParseDuration(*timeoutStr)
	if err != nil {
		fmt.Printf("Error parsing timeout duration: %v\n", err)
		os.Exit(1)
	}

	targets := strings.Split(*targetsStr, ",")
	if len(targets) == 0 {
		fmt.Println("Error: No valid targets provided.")
		os.Exit(1)
	}

	fmt.Println("Initiating Temporal Echo Pings...")

	results := make(chan PingResult, len(targets)**count)
	var wg sync.WaitGroup

	for _, target := range targets {
		wg.Add(1)
		go runPings(target, *count, timeout, results, &wg)
	}

	wg.Wait()
	close(results)

	// Aggregate results
	targetStats := make(map[string]TargetStats)
	for res := range results {
		stats := targetStats[res.Target]
		if stats.Errors == nil {
			stats.Errors = []error{}
		}

		if res.Error == nil {
			stats.Successes++
			if stats.MinLatency == 0 || res.Latency < stats.MinLatency {
				stats.MinLatency = res.Latency
			}
			if res.Latency > stats.MaxLatency {
				stats.MaxLatency = res.Latency
			}
			stats.AvgLatency = (stats.AvgLatency*time.Duration(stats.Successes-1) + res.Latency) / time.Duration(stats.Successes)
		} else {
			stats.Failures++
			stats.Errors = append(stats.Errors, res.Error)
		}
		targetStats[res.Target] = stats
	}

	// Print aggregated results
	for _, target := range targets {
		stats, ok := targetStats[target]
		if !ok {
			// This case should ideally not happen if all targets are processed
			fmt.Printf("\n--- No data for %s ---\n", target)
			continue
		}
		printStats(target, stats)
	}

	fmt.Println("\nTemporal Echo Pings Complete.")
}
