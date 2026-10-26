package main

import (
	"flag"
	"fmt"
	"net"
	"net/url"
	"os"
	"strings"
	"sync"
	"time"
)

var timeout = flag.Duration("timeout", 10*time.Second, "timeout for each probe")

type ProbeResult struct {
	Endpoint string
	Success  bool
	Latency  time.Duration
	Error    string
}

func main() {
	flag.Parse()

	endpoints := flag.Args()
	if len(endpoints) == 0 {
		fmt.Println("Usage: network-probe <endpoint1> <endpoint2> ... [--timeout <duration>]")
		os.Exit(1)
	}

	fmt.Println("Probing endpoints...")

	var wg sync.WaitGroup
	results := make(chan ProbeResult, len(endpoints))

	for _, endpoint := range endpoints {
		wg.Add(1)
		go func(ep string) {
			defer wg.Done()
			results <- probeEndpoint(ep, *timeout)
		}(endpoint)
	}

	wg.Wait()
	close(results)

	for result := range results {
		if result.Success {
			fmt.Printf("[SUCCESS] %s (%s) - Latency: %s\n", result.Endpoint, result.Endpoint, result.Latency)
		} else {
			fmt.Printf("[FAILURE] %s - Error: %s\n", result.Endpoint, result.Error)
		}
	}
}

func probeEndpoint(endpoint string, timeout time.Duration) ProbeResult {
	startTime := time.Now()

	var resolvedAddr string

	// Try to resolve hostname if it's a URL
	if strings.Contains(endpoint, ":") || !strings.Contains(endpoint, ".") {
		// Assume it's a direct IP:port or hostname:port
		resolvedAddr = endpoint
	} else {
		// It looks like a URL, try to parse and resolve
		u, err := url.Parse(endpoint)
		if err != nil {
			return ProbeResult{Endpoint: endpoint, Success: false, Error: fmt.Sprintf("invalid URL: %v", err)}
		}
		// If scheme is missing, default to http for resolution purposes
		parsedEndpoint := endpoint
		if u.Scheme == "" {
			parsedEndpoint = "http://" + endpoint
			u, err = url.Parse(parsedEndpoint)
			if err != nil {
				return ProbeResult{Endpoint: endpoint, Success: false, Error: fmt.Sprintf("invalid URL after defaulting scheme: %v", err)}
			}
		}

		host := u.Hostname()
		port := u.Port()
		if port == "" {
			if u.Scheme == "https" {
				port = "443"
			} else {
				port = "80"
			}
		}
		resolvedAddr = net.JoinHostPort(host, port)
	}

	dialer := net.Dialer{
		Timeout: timeout,
	}

	conn, err := dialer.Dial("tcp", resolvedAddr)
	if err != nil {
		return ProbeResult{Endpoint: endpoint, Success: false, Error: err.Error()}
	}
	defer conn.Close()

	latency := time.Since(startTime)

	return ProbeResult{Endpoint: endpoint, Success: true, Latency: latency}
}
