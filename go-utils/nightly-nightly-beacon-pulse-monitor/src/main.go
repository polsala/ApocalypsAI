package main

import (
	"flag"
	"fmt"
	"io"
	"net"
	"net/http"
	"strings"
	"sync"
	"time"
)

// BeaconResult holds the outcome of a beacon check
type BeaconResult struct {
	Target    string
	Status    string
	Message   string
	Duration  time.Duration
	Error     error
}

// checkHTTP performs an HTTP GET request to the target URL
func checkHTTP(target string, timeout time.Duration) BeaconResult {
	client := http.Client{
		Timeout: timeout,
	}
	start := time.Now()
	resp, err := client.Get(target)
	duration := time.Since(start)

	if err != nil {
		return BeaconResult{
			Target:   target,
			Status:   "Flatlined!",
			Message:  fmt.Sprintf("HTTP request failed: %v", err),
			Duration: duration,
			Error:    err,
		}
	}
	defer resp.Body.Close()

	// Read body to ensure connection is fully closed and measured accurately
	_, _ = io.Copy(io.Discard, resp.Body)

	if resp.StatusCode >= 200 && resp.StatusCode < 400 {
		return BeaconResult{
			Target:   target,
			Status:   "Pulsing strongly!",
			Message:  fmt.Sprintf("%d %s", resp.StatusCode, http.StatusText(resp.StatusCode)),
			Duration: duration,
		}
	}
	return BeaconResult{
		Target:   target,
		Status:   "Faint signal...",
		Message:  fmt.Sprintf("%d %s", resp.StatusCode, http.StatusText(resp.StatusCode)),
		Duration: duration,
	}
}

// checkTCP attempts to establish a TCP connection to host:port
func checkTCP(target string, timeout time.Duration) BeaconResult {
	start := time.Now()
	conn, err := net.DialTimeout("tcp", target, timeout)
	duration := time.Since(start)

	if err != nil {
		return BeaconResult{
			Target:   target,
			Status:   "Flatlined!",
			Message:  fmt.Sprintf("TCP connection failed: %v", err),
			Duration: duration,
			Error:    err,
		}
	}
	defer conn.Close()

	return BeaconResult{
		Target:   target,
		Status:   "Pulsing strongly!",
		Message:  "Connection established",
		Duration: duration,
	}
}

// monitorBeacon determines the type of target and calls the appropriate check function
func monitorBeacon(target string, timeout time.Duration, results chan<- BeaconResult, wg *sync.WaitGroup) {
	defer wg.Done()

	if strings.HasPrefix(target, "http://") || strings.HasPrefix(target, "https://") {
		results <- checkHTTP(target, timeout)
	} else if strings.HasPrefix(target, "tcp:") {
		addr := strings.TrimPrefix(target, "tcp:")
		results <- checkTCP(addr, timeout)
	} else {
		results <- BeaconResult{
			Target:  target,
			Status:  "Unknown Protocol",
			Message: "Target must start with 'http://', 'https://', or 'tcp:'",
			Error:   fmt.Errorf("unsupported target format"),
		}
	}
}

func main() {
	targetsStr := flag.String("targets", "", "Comma-separated list of URLs or tcp:host:port to monitor")
	timeoutStr := flag.String("timeout", "3s", "Timeout for each beacon check (e.g., 1s, 500ms)")
	flag.Parse()

	if *targetsStr == "" {
		fmt.Println("Error: No targets specified. Use -targets flag.")
		flag.Usage()
		return
	}

	targets := strings.Split(*targetsStr, ",")
	timeout, err := time.ParseDuration(*timeoutStr)
	if err != nil {
		fmt.Printf("Error parsing timeout duration: %v\n", err)
		return
	}

	fmt.Printf("Checking %d beacons...\n", len(targets))

	var wg sync.WaitGroup
	results := make(chan BeaconResult, len(targets))

	for _, t := range targets {
		t = strings.TrimSpace(t)
		if t == "" {
			continue
		}
		wg.Add(1)
		go monitorBeacon(t, timeout, results, &wg)
	}

	wg.Wait()
	close(results)

	for res := range results {
		protocol := "UNKNOWN"
		if strings.HasPrefix(res.Target, "http") {
			protocol = "HTTP"
		} else if strings.HasPrefix(res.Target, "tcp") {
			protocol = "TCP"
		}
		fmt.Printf("[%s] %s: %s (%s, %s)\n", protocol, res.Target, res.Status, res.Message, res.Duration.Round(time.Millisecond))
	}
}
