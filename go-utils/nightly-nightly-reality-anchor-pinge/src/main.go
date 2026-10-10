package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
	"sync"
	"time"
)

// PingResult holds the outcome of a single ping operation.
type PingResult struct {
	Host     string
	Port     int
	Duration time.Duration
	Error    error
}

// Pinger defines the interface for pinging a host.
// This allows for easy mocking in tests.
type Pinger interface {
	Ping(host string, port int, timeout time.Duration) (time.Duration, error)
}

// TCPPinger implements Pinger using TCP dial.
type TCPPinger struct{}

// Ping attempts to establish a TCP connection to host:port and measures the time.
func (t *TCPPinger) Ping(host string, port int, timeout time.Duration) (time.Duration, error) {
	address := net.JoinHostPort(host, strconv.Itoa(port))
	start := time.Now()
	conn, err := net.DialTimeout("tcp", address, timeout)
	if err != nil {
		return 0, err
	}
	defer conn.Close()
	return time.Since(start), nil
}

// runPings concurrently pings a list of hosts.
func runPings(hosts []string, port int, timeout time.Duration, pinger Pinger) []PingResult {
	var wg sync.WaitGroup
	resultsChan := make(chan PingResult, len(hosts))

	for _, host := range hosts {
		wg.Add(1)
		go func(h string) {
			defer wg.Done()
			duration, err := pinger.Ping(h, port, timeout)
			resultsChan <- PingResult{Host: h, Port: port, Duration: duration, Error: err}
		}(host)
	}

	wg.Wait()
	close(resultsChan)

	var results []PingResult
	for res := range resultsChan {
		results = append(results, res)
	}
	return results
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: nightly-reality-anchor-pinger <host1> [host2...] [--port=<port>] [--timeout=<duration>]")
		fmt.Println("Example: nightly-reality-anchor-pinger google.com 8.8.8.8 --port=80 --timeout=5s")
		os.Exit(1)
	}

	hosts := []string{}
	port := 80 // Default port
	timeout := 5 * time.Second // Default timeout

	for _, arg := range os.Args[1:] {
		if len(arg) > 7 && arg[:7] == "--port=" {
			p, err := strconv.Atoi(arg[7:])
			if err != nil {
				fmt.Printf("Invalid port: %s. Using default %d.\n", arg[7:], port)
			} else {
				port = p
			}
		} else if len(arg) > 10 && arg[:10] == "--timeout=" {
			d, err := time.ParseDuration(arg[10:])
			if err != nil {
				fmt.Printf("Invalid timeout duration: %s. Using default %s.\n", arg[10:], timeout)
			} else {
				timeout = d
			}
		} else {
			hosts = append(hosts, arg)
		}
	}

	if len(hosts) == 0 {
		fmt.Println("No hosts provided. Usage: nightly-reality-anchor-pinger <host1> [host2...] [--port=<port>] [--timeout=<duration>]")
		os.Exit(1)
	}

	fmt.Printf("Pinging %d reality anchors on port %d with timeout %s...\n", len(hosts), port, timeout)

	results := runPings(hosts, port, timeout, &TCPPinger{})

	fmt.Println("\n--- Reality Anchor Stability Report ---")
	for _, res := range results {
		if res.Error != nil {
			fmt.Printf("  %s:%d - FAILED (%v)\n", res.Host, res.Port, res.Error)
		} else {
			fmt.Printf("  %s:%d - OK (Latency: %s)\n", res.Host, res.Port, res.Duration)
		}
	}
	fmt.Println("-------------------------------------")

	// Exit with non-zero code if any ping failed
	for _, res := range results {
		if res.Error != nil {
			os.Exit(1)
		}
	}
}
