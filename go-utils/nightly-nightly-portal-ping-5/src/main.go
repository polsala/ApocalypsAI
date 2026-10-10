package main

import (
    "flag"
    "fmt"
    "net"
    "sync"
    "time"
)

type dialFunc func(network, address string) (net.Conn, error)

// scanPort attempts to connect to a single port using the provided dial function.
func scanPort(host string, port int, timeout time.Duration, dial dialFunc) bool {
    address := fmt.Sprintf("%s:%d", host, port)
    conn, err := dial("tcp", address)
    if err != nil {
        return false
    }
    conn.Close()
    return true
}

// worker consumes ports from the jobs channel, scans them, and sends open ports to results.
func worker(host string, jobs <-chan int, results chan<- int, wg *sync.WaitGroup, timeout time.Duration, dial dialFunc) {
    defer wg.Done()
    for p := range jobs {
        if scanPort(host, p, timeout, dial) {
            results <- p
        }
    }
}

func main() {
    host := flag.String("host", "", "target hostname or IP (required)")
    start := flag.Int("start", 1, "starting port (inclusive)")
    end := flag.Int("end", 1024, "ending port (inclusive)")
    concurrency := flag.Int("concurrency", 100, "number of concurrent workers")
    timeout := flag.Duration("timeout", 500*time.Millisecond, "dial timeout per port")
    flag.Parse()

    if *host == "" {
        fmt.Println("-host flag is required")
        flag.Usage()
        return
    }
    if *start < 1 || *end > 65535 || *start > *end {
        fmt.Println("invalid port range")
        return
    }

    jobs := make(chan int, *concurrency)
    results := make(chan int, *concurrency)
    var wg sync.WaitGroup

    // Use net.DialTimeout as the real dial function.
    realDial := func(network, address string) (net.Conn, error) {
        return net.DialTimeout(network, address, *timeout)
    }

    // Start workers.
    for i := 0; i < *concurrency; i++ {
        wg.Add(1)
        go worker(*host, jobs, results, &wg, *timeout, realDial)
    }

    // Feed jobs.
    go func() {
        for p := *start; p <= *end; p++ {
            jobs <- p
        }
        close(jobs)
    }()

    // Close results channel when workers are done.
    go func() {
        wg.Wait()
        close(results)
    }()

    // Collect and display open ports.
    for port := range results {
        fmt.Printf("✨ Port %d is open! ✨\n", port)
    }
}
