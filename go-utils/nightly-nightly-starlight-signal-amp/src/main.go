package main

import (
	"flag"
	"fmt"
	"net"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

// DialerFunc is an interface for net.DialTimeout to allow mocking in tests.
type DialerFunc func(network, address string, timeout time.Duration) (net.Conn, error)

// scanPort attempts to connect to a specific port and reports if it's open.
func scanPort(host string, port int, timeout time.Duration, dialer DialerFunc, results chan<- int, wg *sync.WaitGroup) {
	defer wg.Done()
	address := fmt.Sprintf("%s:%d", host, port)
	conn, err := dialer("tcp", address, timeout)
	if err == nil {
		conn.Close()
		results <- port
	}
}

func main() {
	var host string
	var portRangeStr string
	var timeoutSec int

	flag.StringVar(&host, "host", "127.0.0.1", "Target IP address or hostname")
	flag.StringVar(&portRangeStr, "ports", "", "Range of ports to scan (e.g., 1-1024)")
	flag.IntVar(&timeoutSec, "timeout", 1, "Connection timeout in seconds")
	flag.Parse()

	if portRangeStr == "" {
		fmt.Println("Error: --ports argument is required.")
		flag.Usage()
		os.Exit(1)
	}

	parts := strings.Split(portRangeStr, "-")
	if len(parts) != 2 {
		fmt.Println("Error: --ports must be in the format START-END (e.g., 1-1024).")
		os.Exit(1)
	}

	startPort, err := strconv.Atoi(parts[0])
	if err != nil || startPort < 1 || startPort > 65535 {
		fmt.Println("Error: Invalid start port. Must be between 1 and 65535.")
		os.Exit(1)
	}
	endPort, err := strconv.Atoi(parts[1])
	if err != nil || endPort < 1 || endPort > 65535 || endPort < startPort {
		fmt.Println("Error: Invalid end port. Must be between 1 and 65535 and greater than or equal to start port.")
		os.Exit(1)
	}

	timeout := time.Duration(timeoutSec) * time.Second

	fmt.Printf("Starlight Signal Amplifier: Scanning %s from port %d to %d with timeout %s...\n", host, startPort, endPort, timeout)

	var wg sync.WaitGroup
	results := make(chan int, endPort-startPort+1) // Buffered channel for results

	for port := startPort; port <= endPort; port++ {
		wg.Add(1)
		go scanPort(host, port, timeout, net.DialTimeout, results, &wg)
	}

	wg.Wait()    // Wait for all goroutines to finish
	close(results) // Close the channel to signal no more values will be sent

	openPorts := []int{}
	for port := range results {
		openPorts = append(openPorts, port)
	}

	if len(openPorts) == 0 {
		fmt.Println("No open ports found in the specified range.")
	} else {
		fmt.Println("\n--- Amplified Starlight Signals (Open Ports) ---")
		for _, port := range openPorts {
			fmt.Printf("  Port %d is OPEN\n", port)
		}
	}
}
