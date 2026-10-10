package main

import (
	"context"
	"flag"
	"fmt"
	"math"
	"net"
	"strings"
	"sync"
	"time"
)

// Pinger defines an interface for network ping operations.
// # Mock rationale: This interface allows us to mock network calls in tests,
// # preventing actual network requests and ensuring deterministic, offline testing.
type Pinger interface {
	Ping(ctx context.Context, host string, timeout time.Duration) (time.Duration, error)
}

// RealPinger implements Pinger for actual network operations.
type RealPinger struct{}

// Ping attempts to establish a TCP connection to the host:port and measures latency.
// It uses a default port 80 for simplicity, as ICMP requires elevated privileges.
func (rp *RealPinger) Ping(ctx context.Context, host string, timeout time.Duration) (time.Duration, error) {
	addr := net.JoinHostPort(host, "80") // Use port 80 for a common service (HTTP)
	dialer := net.Dialer{Timeout: timeout}

	start := time.Now()
	conn, err := dialer.DialContext(ctx, "tcp", addr)
	if err != nil {
		return 0, fmt.Errorf("failed to dial %s: %w", host, err)
	}
	defer conn.Close()

	return time.Since(start), nil
}

// PingResult holds the results for a single host.
type PingResult struct {
	Host        string
	Latencies   []time.Duration
	AvgLatency  time.Duration
	Jitter      time.Duration
	Entanglement float64
	Error       error
}

// calculateStats computes average latency, jitter, and entanglement score.
func (pr *PingResult) calculateStats() {
	if len(pr.Latencies) == 0 {
		pr.AvgLatency = 0
		pr.Jitter = 0
		pr.Entanglement = 0
		return
	}

	var totalLatency time.Duration
	for _, l := range pr.Latencies {
		totalLatency += l
	}
	pr.AvgLatency = totalLatency / time.Duration(len(pr.Latencies))

	// Calculate jitter (standard deviation)
	var sumSqDiff float64
	for _, l := range pr.Latencies {
		diff := float64(l - pr.AvgLatency)
		sumSqDiff += diff * diff
	}
	variance := sumSqDiff / float64(len(pr.Latencies))
	pr.Jitter = time.Duration(math.Sqrt(variance))

	// Calculate Quantum Entanglement Score
	// Score = 1000 / (AvgLatencyMs + JitterMs + 1)
	// +1 to avoid division by zero if both are 0
	avgMs := float64(pr.AvgLatency.Milliseconds())
	jitterMs := float64(pr.Jitter.Milliseconds())
	pr.Entanglement = 1000.0 / (avgMs + jitterMs + 1.0)
}

func main() {
	hostsStr := flag.String("hosts", "", "Comma-separated list of hosts to ping")
	count := flag.Int("count", 4, "Number of pings per host")
	timeoutStr := flag.String("timeout", "1s", "Timeout for each ping attempt (e.g., 1s, 500ms)")
	flag.Parse()

	if *hostsStr == "" {
		fmt.Println("Error: --hosts is required.")
		flag.Usage()
		return
	}

	hosts := strings.Split(*hostsStr, ",")
	timeout, err := time.ParseDuration(*timeoutStr)
	if err != nil {
		fmt.Printf("Error parsing timeout duration: %v\n", err)
		return
	}

	fmt.Println("🌌 Initiating Quantum Link Test...")

	pinger := &RealPinger{}
	var wg sync.WaitGroup
	resultsChan := make(chan PingResult, len(hosts))

	for _, host := range hosts {
		wg.Add(1)
		go func(h string) {
			defer wg.Done()
			pr := PingResult{Host: h}
			for i := 0; i < *count; i++ {
				ctx, cancel := context.WithTimeout(context.Background(), timeout)
				latency, err := pinger.Ping(ctx, h, timeout)
				cancel()
				if err != nil {
					pr.Error = err
					break // Stop pinging this host on first error
				}
				pr.Latencies = append(pr.Latencies, latency)
				time.Sleep(100 * time.Millisecond) // Small delay between pings
			}
			pr.calculateStats()
			resultsChan <- pr
		}(host)
	}

	wg.Wait()
	close(resultsChan)

	// Collect and print results
	for result := range resultsChan {
		fmt.Printf("\nTesting entanglement with %s (%d pings, timeout %s):\n", result.Host, *count, timeout)
		if result.Error != nil {
			fmt.Printf("  Error: %v\n", result.Error)
		} else if len(result.Latencies) == 0 {
			fmt.Println("  No successful pings.")
		} else {
			fmt.Printf("  Avg Latency: %.2f ms\n", float64(result.AvgLatency.Microseconds())/1000)
			fmt.Printf("  Jitter: %.2f ms\n", float64(result.Jitter.Microseconds())/1000)
			fmt.Printf("  Quantum Entanglement Score: %.1f\n", result.Entanglement)
		}
	}

	fmt.Println("\n✨ Quantum Link Test Complete. May your connections be ever entangled!")
}
