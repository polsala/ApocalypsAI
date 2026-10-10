package main

import (
	"fmt"
	"net"
	"os"
	"sync"
	"time"
)

const (
	connectionTimeout = 2 * time.Second
)

func probeService(target string, wg *sync.WaitGroup, results chan<- string) {
	defer wg.Done()

	conn, err := net.DialTimeout("tcp", target, connectionTimeout)
	if err != nil {
		results <- fmt.Sprintf("[%s] %s is DOWN (%s)", time.Now().Format(time.RFC3339), target, err.Error())
		return
	}

	defer conn.Close()
	results <- fmt.Sprintf("[%s] %s is UP", time.Now().Format(time.RFC3339), target)
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: nightly-go-concurrency-probe <host:port> [<host:port> ...]")
		os.Exit(1)
	}

	targets := os.Args[1:]
	var wg sync.WaitGroup
	results := make(chan string, len(targets))

	fmt.Println("Starting network probes...")

	for _, target := range targets {
		fmt.Printf("[%s] Probing %s...\n", time.Now().Format(time.RFC3339), target)
		wg.Add(1)
		go probeService(target, &wg, results)
	}

	wg.Wait()
	close(results)

	fmt.Println("\n--- Probe Results ---")
	for result := range results {
		fmt.Println(result)
	}
	fmt.Println("---------------------")
}
