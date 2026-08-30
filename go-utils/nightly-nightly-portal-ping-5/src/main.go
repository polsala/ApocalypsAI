package main

import (
    "context"
    "flag"
    "fmt"
    "net"
    "os"
    "runtime"
    "sync"
    "time"
)

// dialContext is a variable so tests can replace it with a mock.
var dialContext = func(ctx context.Context, network, address string) (net.Conn, error) {
    d := net.Dialer{Timeout: 500 * time.Millisecond}
    return d.DialContext(ctx, network, address)
}

// isPortOpen checks whether a TCP port on the given host is open.
func isPortOpen(host string, port int) bool {
    ctx, cancel := context.WithTimeout(context.Background(), 500*time.Millisecond)
    defer cancel()
    address := fmt.Sprintf("%s:%d", host, port)
    conn, err := dialContext(ctx, "tcp", address)
    if err != nil {
        return false
    }
    conn.Close()
    return true
}

// worker receives ports from the jobs channel, scans them, and sends results to the results channel.
func worker(host string, jobs <-chan int, results chan<- string, wg *sync.WaitGroup) {
    defer wg.Done()
    for port := range jobs {
        if isPortOpen(host, port) {
            results <- fmt.Sprintf("✨ Port %d is open! 🎉", port)
        } else {
            results <- fmt.Sprintf("❌ Port %d is closed.", port)
        }
    }
}

func main() {
    host := flag.String("host", "localhost", "Target host to scan")
    start := flag.Int("start", 1, "Start of port range (inclusive)")
    end := flag.Int("end", 1024, "End of port range (inclusive)")
    workers := flag.Int("workers", runtime.NumCPU()*2, "Number of concurrent workers")
    flag.Parse()

    if *start < 1 || *end > 65535 || *start > *end {
        fmt.Fprintln(os.Stderr, "Invalid port range")
        os.Exit(1)
    }

    jobs := make(chan int, *workers)
    results := make(chan string, *end-*start+1)
    var wg sync.WaitGroup

    // Start worker pool
    for i := 0; i < *workers; i++ {
        wg.Add(1)
        go worker(*host, jobs, results, &wg)
    }

    // Enqueue jobs
    go func() {
        for port := *start; port <= *end; port++ {
            jobs <- port
        }
        close(jobs)
    }()

    // Wait for workers to finish then close results channel
    go func() {
        wg.Wait()
        close(results)
    }()

    // Print results as they arrive
    for msg := range results {
        fmt.Println(msg)
    }
}
