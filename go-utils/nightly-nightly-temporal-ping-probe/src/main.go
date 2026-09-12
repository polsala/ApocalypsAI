package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
	"sync"
	"time"
)

// Dialer interface for mocking net.DialTimeout in tests.
type Dialer interface {
	DialTimeout(network, address string, timeout time.Duration) (net.Conn, error)
}

// RealDialer implements Dialer using net.DialTimeout.
type RealDialer struct{}

func (d *RealDialer) DialTimeout(network, address string, timeout time.Duration) (net.Conn, error) {
	return net.DialTimeout(network, address, timeout)
}

// ProbeResult holds the result of a single host probe.
type ProbeResult struct {
	Host      string
	Port      int
	Reachable bool
	Latency   time.Duration
	Timestamp time.Time
	Error     error
}

// probeHost performs a single network probe to a given host:port.
func probeHost(dialer Dialer, host string, port int, timeout time.Duration) ProbeResult {
	address := net.JoinHostPort(host, strconv.Itoa(port))
	start := time.Now()
	conn, err := dialer.DialTimeout("tcp", address, timeout)
	end := time.Now()

	result := ProbeResult{
		Host:      host,
		Port:      port,
		Timestamp: start,
	}

	if err != nil {
		result.Reachable = false
		result.Error = err
	} else {
		result.Reachable = true
		result.Latency = end.Sub(start)
		conn.Close() // Close the connection immediately after successful dial
	}
	return result
}

// runProbes orchestrates concurrent probing of multiple hosts.
func runProbes(dialer Dialer, hosts []string, port int, timeout time.Duration) []ProbeResult {
	var wg sync.WaitGroup
	results := make(chan ProbeResult, len(hosts))

	for _, host := range hosts {
		wg.Add(1)
		go func(h string) {
			defer wg.Done()
			results <- probeHost(dialer, h, port, timeout)
		}(host)
	}

	wg.Wait()
	close(results)

	var allResults []ProbeResult
	for r := range results {
		allResults = append(allResults, r)
	}
	return allResults
}

// currentDialer is a global variable to allow mocking in tests.
var currentDialer Dialer = &RealDialer{}

// osExit is a global variable to allow mocking os.Exit in tests.
var osExit = os.Exit

func main() {
	if len(os.Args) < 3 {
		fmt.Fprintf(os.Stderr, "Usage: %s <port> <host1> [host2...]\n", os.Args[0])
		osExit(1)
	}

	port, err := strconv.Atoi(os.Args[1])
	if err != nil || port <= 0 || port > 65535 {
		fmt.Fprintf(os.Stderr, "Invalid port: %s. Must be a number between 1 and 65535.\n", os.Args[1])
		osExit(1)
	}

	hosts := os.Args[2:]
	timeout := 5 * time.Second // Default timeout for connection attempts

	allResults := runProbes(currentDialer, hosts, port, timeout)

	for _, res := range allResults {
		status := "UNREACHABLE"
		latencyStr := "N/A"
		if res.Reachable {
			status = "REACHABLE"
			latencyStr = fmt.Sprintf("%.2fms", float64(res.Latency)/float64(time.Millisecond))
		}
		fmt.Printf("Host: %s:%d | Status: %s | Latency: %s | Timestamp: %s\n",
			res.Host, res.Port, status, latencyStr, res.Timestamp.Format(time.RFC3339))
	}
}
