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
	timeout := flag.Duration("timeout", 5*time.Second, "timeout for each ping request")
	flag.Parse()

	hosts := flag.Args()

	if len(hosts) == 0 {
		fmt.Println("Usage: ping-probe [-timeout duration] host1 [host2 ...]")
		os.Exit(1)
	}

	var wg sync.WaitGroup
	results := make(chan string, len(hosts))

	for _, host := range hosts {
		wg.Add(1)
		go func(h string) {
			defer wg.Done()
			status := pingHost(h, *timeout)
			results <- fmt.Sprintf("Host: %s - Status: %s", h, status)
		}(host)
	}

	wg.Wait()
	close(results)

	for res := range results {
		fmt.Println(res)
	}
}

func pingHost(host string, timeout time.Duration) string {
	conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), timeout)
	if err != nil {
		if net.IsTimeout(err) {
			return "Unreachable (timeout)"
		}
		return fmt.Sprintf("Unreachable (%v)", err)
	}
	defer conn.Close()
	return "Reachable"
}
