package main

import (
	"fmt"
	"net/http"
	"os"
	"sync"
	"time"
)

// ResonanceResult holds the outcome of a single chronal resonance ping.
type ResonanceResult struct {
	Target   string
	Duration time.Duration
	Error    error
}

// pingTarget performs an HTTP GET request to the given URL and measures the response time.
func pingTarget(target string, client *http.Client) ResonanceResult {
	start := time.Now()
	resp, err := client.Get(target)
	duration := time.Since(start)

	if err != nil {
		return ResonanceResult{Target: target, Duration: duration, Error: err}
	}
	defer resp.Body.Close()

	if resp.StatusCode >= 400 {
		return ResonanceResult{Target: target, Duration: duration, Error: fmt.Errorf("HTTP status %d", resp.StatusCode)}
	}

	return ResonanceResult{Target: target, Duration: duration, Error: nil}
}

// osExit is a variable that can be overridden for testing purposes.
var osExit = os.Exit

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: nightly-chronal-resonance-pinger <target_url_1> [target_url_2 ...]")
		osExit(1)
	}

	targets := os.Args[1:]
	results := make(chan ResonanceResult, len(targets))
	var wg sync.WaitGroup

	// Configure a default HTTP client with a timeout
	httpClient := &http.Client{
		Timeout: 5 * time.Second, // 5-second timeout for each ping
	}

	fmt.Println("Initiating Chronal Resonance Pings...")
	fmt.Println("------------------------------------")

	for _, target := range targets {
		wg.Add(1)
		go func(t string) {
			defer wg.Done()
			results <- pingTarget(t, httpClient)
		}(target)
	}

	wg.Wait()
	close(results)

	var successfulPings []ResonanceResult
	var failedPings []ResonanceResult

	for res := range results {
		if res.Error != nil {
			failedPings = append(failedPings, res)
		} else {
			successfulPings = append(successfulPings, res)
		}
	}

	fmt.Println("\nChronal Resonance Report:")
	fmt.Println("-------------------------")

	if len(successfulPings) > 0 {
		fmt.Println("Successful Resonances:")
		for _, res := range successfulPings {
			fmt.Printf("  [OK] %-30s: %s\n", res.Target, res.Duration)
		}
		fmt.Printf("  Average Resonance Time: %s\n", calculateAverageDuration(successfulPings))
	} else {
		fmt.Println("No successful chronal resonances detected.")
	}

	if len(failedPings) > 0 {
		fmt.Println("\nTemporal Anomalies (Failed Resonances):")
		for _, res := range failedPings {
			fmt.Printf("  [FAIL] %-30s: %v (after %s)\n", res.Target, res.Error, res.Duration)
		}
	} else {
		fmt.Println("\nAll chronal anchors stable. No temporal anomalies detected.")
	}
	fmt.Println("------------------------------------")
}

func calculateAverageDuration(results []ResonanceResult) time.Duration {
	var total time.Duration
	for _, res := range results {
		total += res.Duration
	}
	if len(results) == 0 {
		return 0
	}
	return total / time.Duration(len(results))
}
