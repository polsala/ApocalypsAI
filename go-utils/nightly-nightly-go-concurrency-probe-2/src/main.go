package main

import (
	"fmt"
	"net"
	"os"
	"sync"
	"time"
)

// ServiceStatus represents the status of a network service.
type ServiceStatus struct {
	Address string
	IsUp    bool
}

// probeService attempts to connect to a given network address.
// It returns true if the connection is successful within a timeout, false otherwise.
func probeService(address string, timeout time.Duration) bool {
	conn, err := net.DialTimeout("tcp", address, timeout)
	if err != nil {
		return false
	}
	defer conn.Close()
	return true
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: concurrency_probe <host:port> [<host:port> ...]")
		os.Exit(1)
	}

	addresses := os.Args[1:]
	var wg sync.WaitGroup
	results := make(chan ServiceStatus, len(addresses))

	// Set a reasonable timeout for each probe
	probeTimeout := 2 * time.Second

	for _, addr := range addresses {
		wg.Add(1)
		go func(address string) {
			defer wg.Done()
			isUp := probeService(address, probeTimeout)
			results <- ServiceStatus{Address: address, IsUp: isUp}
		}(addr)
	}

	// Wait for all goroutines to finish
	wg.Wait()
	close(results)

	// Print the results
	for result := range results {
		status := "DOWN"
		if result.IsUp {
			status = "UP"
		}
		fmt.Printf("Service %s is %s\n", result.Address, status)
	}
}
