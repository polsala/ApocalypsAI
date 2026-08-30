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
	Host    string
	Reachable bool
	Error   error
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: concurrent-ping <host1> <host2> ... [timeout]")
		return
	}

	var hosts []string
	var timeout time.Duration = 1 * time.Second // Default timeout

	// Parse arguments, looking for a potential timeout at the end
	for i := 1; i < len(os.Args); i++ {
		arg := os.Args[i]
		if strings.HasSuffix(arg, "ms") || strings.HasSuffix(arg, "s") || strings.HasSuffix(arg, "m") {
			parsedTimeout, err := time.ParseDuration(arg)
			if err == nil {
				timeout = parsedTimeout
				continue // This was the timeout, don't add it to hosts
			}
		}
		hosts = append(hosts, arg)
	}

	if len(hosts) == 0 {
		fmt.Println("No hosts provided to ping.")
		return
	}

	fmt.Printf("Pinging %d hosts with a timeout of %s...
", len(hosts), timeout)

	var wg sync.WaitGroup
	results := make(chan HostStatus, len(hosts))

	for _, host := range hosts {
		wg.Add(1)
		go func(h string) {
			defer wg.Done()
			status := pingHost(h, timeout)
			results <- status
		}(host)
	}

	wg.Wait()
	close(results)

	fmt.Println("\nResults:")
	for result := range results {
		if result.Reachable {
			fmt.Printf("%s: Reachable\n", result.Host)
		} else {
			fmt.Printf("%s: Unreachable (Error: %v)\n", result.Host, result.Error)
		}
	}
}

// pingHost attempts to ping a single host with a given timeout.
func pingHost(host string, timeout time.Duration) HostStatus {
	// For simplicity, we'll use net.DialTimeout to check if a TCP connection can be established.
	// This is a proxy for reachability and doesn't strictly perform an ICMP ping.
	// A real ICMP ping would require root privileges on many systems.

	// Try common ports, or just a generic one if none specified.
	// For this utility, we'll just try a common web port (80) as a proxy.
	address := net.JoinHostPort(host, "80")

	conn, err := net.DialTimeout("tcp", address, timeout)

	if err != nil {
		return HostStatus{Host: host, Reachable: false, Error: err}
	}

	defer conn.Close()
	return HostStatus{Host: host, Reachable: true, Error: nil}
}
