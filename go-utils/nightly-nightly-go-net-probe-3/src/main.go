package main

import (
	"flag"
	"fmt"
	"net"
	"os"
	"sync"
	"time"
)

func main() {
	t
	timeout := flag.Duration("timeout", 5*time.Second, "timeout for each probe")
	flag.Parse()

	endpoints := flag.Args()
	if len(endpoints) == 0 {
		fmt.Println("Usage: netprobe [-timeout duration] <endpoint1> <endpoint2> ...")
		os.Exit(1)
	}

	var wg sync.WaitGroup

	for _, endpoint := range endpoints {
		wg.Add(1)
		go func(ep string) {
			defer wg.Done()
			probeEndpoint(ep, *timeout)
		}(endpoint)
	}

	wg.Wait()
}

func probeEndpoint(endpoint string, timeout time.Duration) {
	start := time.Now()
	conn, err := net.DialTimeout("tcp", endpoint, timeout)

	if err != nil {
		fmt.Printf("Endpoint: %s, Status: DOWN, Latency: N/A (Error: %v)\n", endpoint, err)
		return
	}

	defer conn.Close()

	duration := time.Since(start)
	fmt.Printf("Endpoint: %s, Status: UP, Latency: %s\n", endpoint, duration.RoundTo(time.Millisecond))
}
