package main

import (
	"fmt"
	"net/http"
	"sync"
	"time"
)

// Target defines an endpoint to check and its expected maximum response duration.
type Target struct {
	URL                 string
	ExpectedMaxDurationMs int
}

// Result stores the outcome of a target check.
type Result struct {
	Target   Target
	Duration time.Duration
	Status   string
	Error    error
}

const (
	// SlightAnomalyFactor defines the multiplier for 'Slight Chronal Anomaly' threshold.
	SlightAnomalyFactor = 1.5
	// SevereDilationFactor defines the multiplier for 'Severe Time Dilation' threshold.
	SevereDilationFactor = 3.0
)

// checkTarget performs an HTTP GET request to the target URL and measures the response time.
func checkTarget(client *http.Client, target Target) Result {
	start := time.Now()
	req, err := http.NewRequest("GET", target.URL, nil)
	if err != nil {
		return Result{Target: target, Status: "Lost in the Void", Error: fmt.Errorf("failed to create request: %w", err)}
	}

	resp, err := client.Do(req)
	if err != nil {
		return Result{Target: target, Status: "Lost in the Void", Error: fmt.Errorf("connection error: %w", err)}
	}
	defer resp.Body.Close()

	duration := time.Since(start)

	expectedDuration := time.Duration(target.ExpectedMaxDurationMs) * time.Millisecond

	status := "Temporal Harmony"
	if duration > expectedDuration*time.Duration(SevereDilationFactor) {
		status = "Severe Time Dilation"
	} else if duration > expectedDuration*time.Duration(SlightAnomalyFactor) {
		status = "Slight Chronal Anomaly"
	} else if duration > expectedDuration {
		// If it's just over expected but not yet a 'Slight Anomaly'
		status = "Slight Chronal Anomaly"
	}

	return Result{Target: target, Duration: duration, Status: status, Error: nil}
}

func main() {
	fmt.Println("Initiating Chrono-Sync Scan...")

	// Define the targets to monitor.
	// Modify this slice to add/remove/change endpoints and their expected durations.
	var targets = []Target{
		{URL: "http://localhost:8080/status", ExpectedMaxDurationMs: 100},
		{URL: "https://example.com", ExpectedMaxDurationMs: 200},
		{URL: "http://nonexistent.local", ExpectedMaxDurationMs: 50},
		{URL: "https://httpbin.org/delay/0.05", ExpectedMaxDurationMs: 10},
		{URL: "https://httpbin.org/delay/0.2", ExpectedMaxDurationMs: 50},
		{URL: "https://httpbin.org/status/500", ExpectedMaxDurationMs: 100},
	}

	var wg sync.WaitGroup
	results := make(chan Result, len(targets))

	client := &http.Client{
		Timeout: 5 * time.Second, // Global timeout for HTTP requests
	}

	for _, target := range targets {
		wg.Add(1)
		go func(t Target) {
			defer wg.Done()
			results <- checkTarget(client, t)
		}(target)
	}

	wg.Wait()
	close(results)

	fmt.Println("\nChrono-Sync Scan Results:")
	for res := range results {
		if res.Error != nil {
			fmt.Printf("[%s] %s (%v)\n", res.Target.URL, res.Status, res.Error)
		} else {
			expectedDuration := time.Duration(res.Target.ExpectedMaxDurationMs) * time.Millisecond
			if res.Status == "Temporal Harmony" {
				fmt.Printf("[%s] %s (%v)\n", res.Target.URL, res.Status, res.Duration)
			} else {
				fmt.Printf("[%s] %s (%v, expected <%v)\n", res.Target.URL, res.Status, res.Duration, expectedDuration)
			}
		}
	}

	fmt.Println("\nChrono-Sync Scan Complete. All temporal anomalies logged.")
}
