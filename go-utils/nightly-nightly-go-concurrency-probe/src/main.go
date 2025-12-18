package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
	"sync"
	"time"
)

func main() {
	if len(os.Args) != 5 {
		fmt.Fprintf(os.Stderr, "Usage: %s <host> <port> <num_connections> <duration_seconds>\n", os.Args[0])
		os.Exit(1)
	}

	host := os.Args[1]
	port := os.Args[2]
	numConnections, err := strconv.Atoi(os.Args[3])
	if err != nil {
		fmt.Fprintf(os.Stderr, "Invalid number of connections: %v\n", err)
		os.Exit(1)
	}
	durationSeconds, err := strconv.Atoi(os.Args[4])
	if err != nil {
		fmt.Fprintf(os.Stderr, "Invalid duration: %v\n", err)
		os.Exit(1)
	}

	address := net.JoinHostPort(host, port)
	fmt.Printf("Probing %s with %d concurrent connections for %d seconds...\n", address, numConnections, durationSeconds)

	var wg sync.WaitGroup
	succesfulConnections := 0
	failedConnections := 0
	var mu sync.Mutex

	stopCh := make(chan struct{})
	go func() {
		time.Sleep(time.Duration(durationSeconds) * time.Second)
		close(stopCh)
		fmt.Println("\nProbe duration ended.")
	}()

	for i := 0; i < numConnections; i++ {
		wg.Add(1)
		go func(connID int) {
			defer wg.Done()
			select {
			case <-stopCh:
				return // Stop this goroutine if the probe duration is over
			default:
				conn, err := net.DialTimeout("tcp", address, 2*time.Second) // Short timeout for each connection attempt
				if err != nil {
					mu.Lock()
					failedConnections++
					mu.Unlock()
					// fmt.Fprintf(os.Stderr, "Connection %d failed: %v\n", connID, err)
					return
				}
			defer conn.Close()

			mu.Lock()
			succesfulConnections++
			mu.Unlock()
			// Keep connection open for a short while to simulate active use
			select {
			case <-time.After(500 * time.Millisecond): // Keep connection alive briefly
			case <-stopCh:
				return
			}
		}(i)
	}

	wg.Wait()

	fmt.Printf("\n--- Probe Results ---\n")
	fmt.Printf("Total connections attempted: %d\n", numConnections)
	fmt.Printf("Successful connections: %d\n", succesfulConnections)
	fmt.Printf("Failed connections: %d\n", failedConnections)
	fmt.Printf("---------------------\n")
}
