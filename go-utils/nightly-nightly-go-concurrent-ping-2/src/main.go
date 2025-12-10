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
	timeout := flag.Duration("timeout", 1*time.Second, "timeout for each ping request")
	flag.Parse()

	hosts := flag.Args()

	if len(hosts) == 0 {
		fmt.Println("Usage: concurrent-ping [-timeout duration] host1 [host2 ...]")
		os.Exit(1)
	}

	var wg sync.WaitGroup

	results := make(chan string, len(hosts))

	for _, host := range hosts {
		wg.Add(1)
		go func(h string) {
			defer wg.Done()
			pingHost(h, *timeout, results)
		}(host)
	}

	wg.Wait()
	close(results)

	for res := range results {
		fmt.Print(res)
	}
}

func pingHost(host string, timeout time.Duration, results chan<- string) {
	start := time.Now()

	// Attempt to resolve the hostname first to get an IP address
	addrs, err := net.LookupHost(host)

	var ipAddr string
	if err != nil {
		ipAddr = "(resolution failed)"
	} else {
		ipAddr = addrs[0] // Use the first resolved IP
	}

	conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), timeout)
	if err != nil {
		results <- fmt.Sprintf("Pinging %s (%s)...
  Failed: %s: %v (timeout: %v)\n\n", host, ipAddr, host, err, timeout)
		return
	}

	defer conn.Close()
	duration := time.Since(start)

	results <- fmt.Sprintf("Pinging %s (%s)...
  Success: %s is reachable in %v\n\n", host, ipAddr, host, duration)
}
