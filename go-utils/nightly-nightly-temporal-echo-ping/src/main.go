package main

import (
	"fmt"
	"net/http"
	"time"
	"sync"
	"os"
	"strconv"
	"strings"
)

// Target represents a temporal anchor to monitor.
type Target struct {
	Name string
	URL  string
}

// PingResult stores the outcome of a ping operation.
type PingResult struct {
	TargetName string
	Latency    time.Duration
	Error      error
	IsEcho     bool // True if latency is anomalous
}

// pingTarget performs an HTTP GET request to the target URL and measures latency.
func pingTarget(target Target, timeout time.Duration) PingResult {
	client := &http.Client{
		Timeout: timeout,
	}

	start := time.Now()
	resp, err := client.Get(target.URL)
	latency := time.Since(start)

	if err != nil {
		return PingResult{TargetName: target.Name, Error: err, Latency: latency}
	}
	defer resp.Body.Close()

	// Consider non-2xx status codes as errors for simplicity, or just report them.
	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		return PingResult{TargetName: target.Name, Error: fmt.Errorf("non-2xx status code: %d", resp.StatusCode), Latency: latency}
	}

	return PingResult{TargetName: target.Name, Latency: latency}
}

// monitorTargets concurrently pings a list of targets and returns their results.
func monitorTargets(targets []Target, timeout time.Duration, echoThresholdMs int) []PingResult {
	var wg sync.WaitGroup
	results := make(chan PingResult, len(targets))

	for _, target := range targets {
		wg.Add(1)
		go func(t Target) {
			defer wg.Done()
			result := pingTarget(t, timeout)
			if result.Error == nil && result.Latency.Milliseconds() > int64(echoThresholdMs) {
				result.IsEcho = true
			}
			results <- result
		}(target)
	}

	wg.Wait()
	close(results)

	var allResults []PingResult
	for res := range results {
		allResults = append(allResults, res)
	}
	return allResults
}

func main() {
	// Configuration from environment variables or defaults
	targetsStr := os.Getenv("TEMPORAL_ANCHORS")
	if targetsStr == "" {
		targetsStr = "Void Gate=http://localhost:8080/void,Rift Stabilizer=http://localhost:8081/rift"
	}

	timeoutStr := os.Getenv("PING_TIMEOUT_MS")
	timeoutMs, err := strconv.Atoi(timeoutStr)
	if err != nil || timeoutMs <= 0 {
		timeoutMs = 5000 // Default to 5 seconds
	}
	pingTimeout := time.Duration(timeoutMs) * time.Millisecond

	echoThresholdStr := os.Getenv("ECHO_THRESHOLD_MS")
	echoThresholdMs, err := strconv.Atoi(echoThresholdStr)
	if err != nil || echoThresholdMs <= 0 {
		echoThresholdMs = 200 // Default to 200ms
	}

	var targets []Target
	for _, t := range strings.Split(targetsStr, ",") {
		parts := strings.SplitN(t, "=", 2)
		if len(parts) == 2 {
			targets = append(targets, Target{Name: parts[0], URL: parts[1]})
		} else {
			fmt.Fprintf(os.Stderr, "Warning: Invalid target format '%s'. Expected 'Name=URL'. Skipping.\n", t)
		}
	}

	if len(targets) == 0 {
		fmt.Println("No temporal anchors configured. Exiting.")
		os.Exit(1)
	}

	fmt.Printf("Monitoring %d temporal anchors for stability...\n", len(targets))
	fmt.Printf("Ping Timeout: %s, Echo Threshold: %dms\n", pingTimeout, echoThresholdMs)

	allResults := monitorTargets(targets, pingTimeout, echoThresholdMs)

	fmt.Println("\n--- Temporal Stability Report ---")
	hasEchoes := false
	for _, res := range allResults {
		if res.Error != nil {
			fmt.Printf("  [ERROR] %s: Temporal link severed! (%v)\n", res.TargetName, res.Error)
		} else if res.IsEcho {
			fmt.Printf("  [ECHO!] %s: Experiencing temporal flux! Latency: %s (exceeds %dms)\n", res.TargetName, res.Latency, echoThresholdMs)
			hasEchoes = true
		} else {
			fmt.Printf("  [OK]    %s: Temporal stability maintained. Latency: %s\n", res.TargetName, res.Latency)
		}
	}

	if hasEchoes {
		fmt.Println("\nWarning: Some temporal anchors are experiencing echoes. Investigation recommended.")
		os.Exit(1) // Indicate an issue
	} else {
		fmt.Println("\nAll temporal anchors are stable. The timeline holds... for now.")
	}
}
