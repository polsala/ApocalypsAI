package main

import (
	"fmt"
	"net"
	"os"
	"strings"
	"sync"
	"time"
)

// HostStatus represents the status of a pinged host.
type HostStatus struct {
	Host      string
	Status    string
	Duration  time.Duration
	ErrorMsg  string
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: concurrent-ping <host1,host2,...>")
		os.Exit(1)
	}

	hosts := strings.Split(os.Args[1], ",")
	var wg sync.WaitGroup
	results := make(chan HostStatus, len(hosts))

	for _, host := range hosts {
		wg.Add(1)
		go pingHost(host, &wg, results)
	}

	wg.Wait()
	close(results)

	// Print results in a somewhat ordered fashion (though channel order isn't guaranteed)
	// For deterministic output in tests, we'll sort later.
	var finalStatuses []HostStatus
	for status := range results {
		finalStatuses = append(finalStatuses, status)
	}

	// Sort results by original host order for consistent output
	// This is a bit of a hack for deterministic output, in a real-world scenario
	// order might not matter as much.
	ssortedStatuses := make([]HostStatus, len(hosts))
	for _, s := range finalStatuses {
		for i, originalHost := range hosts {
			if s.Host == originalHost {
				sortedStatuses[i] = s
				break
			}
		}
	}

	for _, status := range sortedStatuses {
		if status.ErrorMsg != "" {
			fmt.Printf("Host: %s, Status: ERROR, Error: %s\n", status.Host, status.ErrorMsg)
		} else {
			fmt.Printf("Host: %s, Status: %s, Time: %s\n", status.Host, status.Status, status.Duration.String())
		}
	}
}

func pingHost(host string, wg *sync.WaitGroup, results chan<- HostStatus) {
	defer wg.Done()

	startTime := time.Now()

	// Try to resolve the host first to catch DNS errors early
	_, err := net.LookupHost(host)
	if err != nil {
		results <- HostStatus{
			Host:     host,
			Status:   "ERROR",
			Duration: time.Since(startTime),
			ErrorMsg: err.Error(),
		}
		return
	}

	// For simplicity, we'll use a TCP dial with a short timeout as a proxy for ping.
	// A true ICMP ping would require elevated privileges or specific libraries.
	// This approach is more universally applicable.
	conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), 2*time.Second) // Using port 80 for simplicity
	
	status := "UP"
	if err != nil {
		status = "DOWN"
	} else {
		conn.Close()
	}

	results <- HostStatus{
		Host:     host,
		Status:   status,
		Duration: time.Since(startTime),
		ErrorMsg: "",
	}
}
