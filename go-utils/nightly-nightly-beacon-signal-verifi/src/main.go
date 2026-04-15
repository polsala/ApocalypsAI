package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

// Pinger interface for mocking network calls
type Pinger interface {
	Ping(host string, port int, timeout time.Duration) PingResult
}

// RealPinger implements Pinger for actual network operations
type RealPinger struct{}

func (rp *RealPinger) Ping(host string, port int, timeout time.Duration) PingResult {
	address := net.JoinHostPort(host, strconv.Itoa(port))
	start := time.Now()
	conn, err := net.DialTimeout("tcp", address, timeout)
	if err != nil {
		return PingResult{
			Host:    host,
			Port:    port,
			Success: false,
			Error:   err.Error(),
		}
	}
	defer conn.Close()
	duration := time.Since(start)
	return PingResult{
		Host:    host,
		Port:    port,
		Success: true,
		Latency: duration,
	}
}

// PingResult holds the outcome of a single beacon ping
type PingResult struct {
	OriginalBeacon string // Store the original string for reporting invalid formats
	Host           string
	Port           int
	Success        bool
	Latency        time.Duration
	Error          string
}

// parseBeacon parses a "host:port" string into host and port.
func parseBeacon(beaconStr string) (string, int, error) {
	parts := strings.Split(beaconStr, ":")
	if len(parts) != 2 {
		return "", 0, fmt.Errorf("invalid format. Expected host:port")
	}
	port, err := strconv.Atoi(parts[1])
	if err != nil {
		return "", 0, fmt.Errorf("invalid port number '%s'", parts[1])
	}
	return parts[0], port, nil
}

// runVerification orchestrates the concurrent pinging of beacons.
func runVerification(pinger Pinger, beaconStrings []string, timeout time.Duration) []PingResult {
	var wg sync.WaitGroup
	resultsChan := make(chan PingResult, len(beaconStrings)) // Buffered channel

	for _, beaconStr := range beaconStrings {
		host, port, err := parseBeacon(beaconStr)
		if err != nil {
			resultsChan <- PingResult{
				OriginalBeacon: beaconStr,
				Success:        false,
				Error:          fmt.Sprintf("Invalid beacon '%s': %v", beaconStr, err),
			}
			continue
		}

		wg.Add(1)
		go func(h string, p int, original string) {
			defer wg.Done()
			result := pinger.Ping(h, p, timeout)
			result.OriginalBeacon = original // Ensure original beacon string is always set
			resultsChan <- result
		}(host, port, beaconStr)
	}

	wg.Wait()      // Wait for all goroutines to finish
	close(resultsChan) // Close the channel to signal no more writes

	var finalResults []PingResult
	for result := range resultsChan { // Read all results from the channel
		finalResults = append(finalResults, result)
	}
	return finalResults
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: nightly-beacon-signal-verifier <beacon1> [beacon2...] [--timeout=<duration>]")
		fmt.Println("Example: nightly-beacon-signal-verifier google.com:80 example.com:443 --timeout=5s")
		os.Exit(1)
	}

	beaconStrings := []string{}
	timeout := 3 * time.Second // Default timeout
	
	// Parse command-line arguments
	for _, arg := range os.Args[1:] {
		if strings.HasPrefix(arg, "--timeout=") {
			durationStr := strings.TrimPrefix(arg, "--timeout=")
			parsedTimeout, err := time.ParseDuration(durationStr)
			if err != nil {
				fmt.Printf("Error: Invalid timeout duration '%s': %v\n", durationStr, err)
				os.Exit(1)
			}
			timeout = parsedTimeout
		} else {
			beaconStrings = append(beaconStrings, arg)
		}
	}

	if len(beaconStrings) == 0 {
		fmt.Println("Error: No beacons provided. Usage: nightly-beacon-signal-verifier <beacon1> [beacon2...] [--timeout=<duration>]")
		os.Exit(1)
	}

	pinger := &RealPinger{} // Use the real pinger for main execution
	finalResults := runVerification(pinger, beaconStrings, timeout)

	fmt.Println("\n--- Beacon Signal Verification Report ---")
	allUp := true
	for _, result := range finalResults {
		if result.Success {
			fmt.Printf("✅ %s:%d - UP (Latency: %s)\n", result.Host, result.Port, result.Latency.Round(time.Millisecond))
		} else {
			// Report using OriginalBeacon for clarity, especially for parse errors
			fmt.Printf("❌ %s - DOWN (Error: %s)\n", result.OriginalBeacon, result.Error)
			allUp = false
		}
	}
	fmt.Println("-----------------------------------------")

	if !allUp {
		os.Exit(1) // Exit with non-zero code if any beacon is down or invalid
	}
}
