package main

import (
	"fmt"
	"net/http"
	"time"
	"os"
	"strings"
	"sync"
	"strconv"
)

// RippleReport captures the outcome of a network probe.
type RippleReport struct {
	Target    string
	Status    string
	Latency   time.Duration
	Error     error
	IsRipple  bool
	Message   string
}

// probeTarget sends an HTTP GET request to a target and measures latency.
func probeTarget(target string, timeout time.Duration, results chan<- RippleReport, wg *sync.WaitGroup, latencyThresholdMs int) {
	defer wg.Done()

	report := RippleReport{Target: target}
	client := http.Client{
		Timeout: timeout,
	}

	start := time.Now()
	resp, err := client.Get(target)
	report.Latency = time.Since(start)

	if err != nil {
		report.Error = err
		report.Status = "ERROR"
		report.IsRipple = true
		report.Message = fmt.Sprintf("Failed to connect: %v", err)
	} else {
		defer resp.Body.Close()
		report.Status = resp.Status
		if resp.StatusCode >= 400 || report.Latency.Milliseconds() > int64(latencyThresholdMs) {
			report.IsRipple = true
			if resp.StatusCode >= 400 {
				report.Message = fmt.Sprintf("Received an unstable resonance (HTTP %s)", resp.Status)
			} else {
				report.Message = fmt.Sprintf("Detected a temporal distortion (high latency: %s)", report.Latency)
			}
		} else {
			report.Message = fmt.Sprintf("Reported a stable resonance (HTTP %s, Latency: %s)", resp.Status, report.Latency)
		}
	}
	results <- report
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: nightly-net-ripple-detector <target1_url> [target2_url...] [--timeout=<ms>] [--threshold=<ms>]")
		os.Exit(1)
	}

	targets := []string{}
	timeoutMs := 5000 // Default timeout 5 seconds
	latencyThresholdMs := 1000 // Default latency threshold 1 second

	for _, arg := range os.Args[1:] {
		if strings.HasPrefix(arg, "--timeout=") {
			valStr := strings.TrimPrefix(arg, "--timeout=")
			val, err := strconv.Atoi(valStr)
			if err == nil && val > 0 {
				timeoutMs = val
			} else {
				fmt.Fprintf(os.Stderr, "Warning: Invalid timeout value '%s', using default %dms.\n", valStr, timeoutMs)
			}
		} else if strings.HasPrefix(arg, "--threshold=") {
			valStr := strings.TrimPrefix(arg, "--threshold=")
			val, err := strconv.Atoi(valStr)
			if err == nil && val > 0 {
				latencyThresholdMs = val
			} else {
				fmt.Fprintf(os.Stderr, "Warning: Invalid threshold value '%s', using default %dms.\n", valStr, latencyThresholdMs)
			}
		} else {
			targets = append(targets, arg)
		}
	}

	if len(targets) == 0 {
		fmt.Println("No targets specified. Usage: nightly-net-ripple-detector <target1_url> [target2_url...] [--timeout=<ms>] [--threshold=<ms>]")
		os.Exit(1)
	}

	timeout := time.Duration(timeoutMs) * time.Millisecond
	fmt.Printf("Detecting etheric ripples across %d targets (Timeout: %s, Latency Threshold: %dms)...\n", len(targets), timeout, latencyThresholdMs)

	results := make(chan RippleReport, len(targets))
	var wg sync.WaitGroup

	for _, target := range targets {
		wg.Add(1)
		go probeTarget(target, timeout, results, &wg, latencyThresholdMs)
	}

	wg.Wait()
	close(results)

	rippleDetected := false
	fmt.Println("\n--- Ripple Detection Report ---")
	for report := range results {
		if report.IsRipple {
			rippleDetected = true
			fmt.Printf("[RIPPLE DETECTED] %s: %s\n", report.Target, report.Message)
		} else {
			fmt.Printf("[STABLE] %s: %s\n", report.Target, report.Message)
		}
	}

	if rippleDetected {
		fmt.Println("\nWarning: One or more etheric ripples detected in the network fabric!")
		os.Exit(1) // Indicate failure
	} else {
		fmt.Println("\nAll network resonances are stable. No etheric ripples detected.")
		os.Exit(0) // Indicate success
	}
}
