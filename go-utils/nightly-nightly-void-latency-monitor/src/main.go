package main

import (
	"fmt"
	"net"
	"sync"
	"time"
)

// Endpoint represents a target to monitor
type Endpoint struct {
	Name    string
	Address string // host:port
}

// PingResult stores the outcome of a single ping attempt
type PingResult struct {
	EndpointName string
	Latency      time.Duration
	Success      bool
	Error        error
}

// Pinger interface for mocking network operations
type Pinger interface {
	Ping(address string, timeout time.Duration) PingResult
}

// TCPPinger implements Pinger for TCP connections
type TCPPinger struct{}

func (t *TCPPinger) Ping(address string, timeout time.Duration) PingResult {
	start := time.Now()
	conn, err := net.DialTimeout("tcp", address, timeout)
	if err != nil {
		return PingResult{
			Latency:      time.Since(start),
			Success:      false,
			Error:        err,
		}
	}
	defer conn.Close()
	return PingResult{
		Latency: time.Since(start),
		Success: true,
		Error:   nil,
	}
}

// Monitor performs concurrent pings and aggregates results
func Monitor(endpoints []Endpoint, pinger Pinger, timeout time.Duration, count int) map[string][]PingResult {
	var wg sync.WaitGroup
	resultsChan := make(chan PingResult, len(endpoints)*count)
	allResults := make(map[string][]PingResult)
	var mu sync.Mutex // To protect allResults map

	for _, ep := range endpoints {
		for i := 0; i < count; i++ {
			wg.Add(1)
			go func(endpoint Endpoint) {
				defer wg.Done()
				res := pinger.Ping(endpoint.Address, timeout)
				res.EndpointName = endpoint.Name
				resultsChan <- res
			}(ep)
		}
	}

	wg.Wait()
	close(resultsChan)

	for res := range resultsChan {
		mu.Lock()
		allResults[res.EndpointName] = append(allResults[res.EndpointName], res)
		mu.Unlock()
	}
	return allResults
}

func main() {
	// Default endpoints (can be configured via CLI args in a real app)
	endpoints := []Endpoint{
		{Name: "The Void", Address: "example.com:80"}, // Using example.com for a real-world test
		{Name: "Temporal Rift Gateway", Address: "nonexistent.invalid:80"}, // Will likely fail
		{Name: "Echo Chamber Nexus", Address: "google.com:443"},
	}
	timeout := 2 * time.Second
	pingCount := 3

	fmt.Println("Initiating Void Latency Monitoring...")
	fmt.Printf("Monitoring %d endpoints, %d pings each, with %s timeout.\n", len(endpoints), pingCount, timeout)

	pinger := &TCPPinger{}
	results := Monitor(endpoints, pinger, timeout, pingCount)

	fmt.Println("\n--- Void Latency Report ---")
	for name, resList := range results {
		totalLatency := time.Duration(0)
		successCount := 0
		minLatency := timeout * 100 // Arbitrarily large initial value
		maxLatency := time.Duration(0)

		for _, r := range resList {
			if r.Success {
				successCount++
				totalLatency += r.Latency
				if r.Latency < minLatency {
					minLatency = r.Latency
				}
				if r.Latency > maxLatency {
					maxLatency = r.Latency
				}
			}
		}

		fmt.Printf("\nEndpoint: %s (%s)\n", name, func() string { // Inline function to find address
			for _, ep := range endpoints {
				if ep.Name == name {
					return ep.Address
				}
			}
			return "unknown"
		}())
		fmt.Printf("  Pings Sent: %d\n", len(resList))
		fmt.Printf("  Successful: %d (%.2f%%)\n", successCount, float64(successCount)/float64(len(resList))*100)
		if successCount > 0 {
			fmt.Printf("  Avg Latency: %s\n", totalLatency/time.Duration(successCount))
			fmt.Printf("  Min Latency: %s\n", minLatency)
			fmt.Printf("  Max Latency: %s\n", maxLatency)
		} else {
			fmt.Println("  No successful pings.")
		}
		// Whimsical stability score
		if successCount == len(resList) && totalLatency/time.Duration(successCount) < 500*time.Millisecond {
			fmt.Println("  Temporal Stability: HIGH - The Void is calm.")
		} else if successCount > 0 {
			fmt.Println("  Temporal Stability: MODERATE - Minor ripples detected.")
		} else {
			fmt.Println("  Temporal Stability: LOW - The fabric of reality is tearing!")
		}
	}
}
