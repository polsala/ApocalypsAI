package main

import (
	"context"
	"flag"
	"fmt"
	"net"
	"os"
	"sync"
	"time"
)

func pingHost(ctx context.Context, host string, results chan<- string, wg *sync.WaitGroup) {
	defer wg.Done()

	// We'll try to connect to port 80 as a proxy for reachability.
	// For a true ICMP ping, we'd need root privileges or a different approach.
	// This TCP connect is a good enough indicator for many use cases.
	conn, err := net.DialTimeout("tcp", host+":80", 5*time.Second) // Default dial timeout

	select {
	case <-ctx.Done():
		results <- fmt.Sprintf("%s: Timed out (context cancelled)", host)
		return
	default:
		// Continue if context is not done
	}

	if err != nil {
		results <- fmt.Sprintf("%s: Unreachable (%v)", host, err)
		return
	}

	defer conn.Close()
	results <- fmt.Sprintf("%s: Reachable", host)
}

func main() {
	timeout := flag.Duration("timeout", 10*time.Second, "timeout for each ping in seconds")
	flag.Parse()

	hosts := flag.Args()
	if len(hosts) == 0 {
		fmt.Println("Usage: concurrent-ping [-timeout duration] host1 [host2 ...]")
		os.Exit(1)
	}

	var wg sync.WaitGroup
	results := make(chan string, len(hosts))

	ctx, cancel := context.WithTimeout(context.Background(), *timeout)
	defer cancel() // Ensure cancel is called to release resources

	for _, host := range hosts {
		wg.Add(1)
		go pingHost(ctx, host, results, &wg)
	}

	wg.Wait()
	close(results)

	fmt.Println("--- Ping Results ---")
	for result := range results {
		fmt.Println(result)
	}
	fmt.Println("--------------------")
}
