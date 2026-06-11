package main

import (
	"flag"
	"fmt"
	"net"
	"os"
	"sync"
	"time"
)

// HostStatus represents the status of a pinged host.
type HostStatus struct {
	Host    string
	IsUp    bool
	Latency time.Duration
	Error   error
}

func main() {
	timeout := flag.Duration("timeout", 1*time.Second, "timeout for each ping")
	flag.Parse()

	hosts := flag.Args()
	if len(hosts) == 0 {
		fmt.Println("Usage: concurrent-ping [-timeout=duration] host1 host2 ...")
		os.Exit(1)
	}

	var wg sync.WaitGroup
	results := make(chan HostStatus, len(hosts))

	for _, host := range hosts {
		wg.Add(1)
		go func(h string) {
			defer wg.Done()
			status := pingHost(h, *timeout)
			results <- status
		}(host)
	}

	wg.Wait()
	close(results)

	fmt.Println("--- Ping Results ---")
	for result := range results {
		if result.Error != nil {
			fmt.Printf("%s: DOWN (Error: %v)\n", result.Host, result.Error)
		} else if result.IsUp {
			fmt.Printf("%s: UP (Latency: %s)\n", result.Host, result.Latency.RoundTo(time.Millisecond))
		} else {
			fmt.Printf("%s: DOWN (Timeout)\n", result.Host)
		}
	}
	fmt.Println("--------------------")
}

// pingHost attempts to ping a single host.
func pingHost(host string, timeout time.Duration) HostStatus {
	startTime := time.Now()

	// Use DialTimeout to check if the host is reachable within the timeout.
	// This is a simplified check, not a true ICMP ping.
	conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), timeout)
	
	// Mock rationale: In a real scenario, we'd use a more robust ping mechanism (like ICMP).
	// For this example and testing, DialTimeout on a common port (like 80) serves as a proxy
	// for network reachability and is easier to mock.

	if err != nil {
		return HostStatus{
			Host:  host,
			IsUp:  false,
			Error: err,
		}
	}

	defer conn.Close()

	latency := time.Since(startTime)

	return HostStatus{
		Host:    host,
		IsUp:    true,
		Latency: latency,
	}
}
