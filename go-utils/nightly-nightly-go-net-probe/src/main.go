package main

import (
	"fmt"
	"net"
	"os"
	"sync"
	"time"
)

func probeEndpoint(endpoint string, wg *sync.WaitGroup, results chan<- string) {
	defer wg.Done()

	startTime := time.Now()

	conn, err := net.DialTimeout("tcp", endpoint, 5*time.Second) // 5-second timeout
	if err != nil {
		results <- fmt.Sprintf("Probing %s...\n  -> Unreachable (Error: %v)", endpoint, err)
		return
	}
	defer conn.Close()

	latency := time.Since(startTime)
	results <- fmt.Sprintf("Probing %s...\n  -> Reachable (Latency: %s)", endpoint, latency.Round(time.Millisecond))
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: netprobe <endpoint1> <endpoint2> ...")
		fmt.Println("Example: netprobe google.com:80 example.com:443")
		os.Exit(1)
	}

	endpoints := os.Args[1:]

	var wg sync.WaitGroup
	results := make(chan string, len(endpoints))

	for _, endpoint := range endpoints {
		wg.Add(1)
		go probeEndpoint(endpoint, &wg, results)
	}

	wg.Wait()
	close(results)

	for result := range results {
		fmt.Println(result)
	}
}
