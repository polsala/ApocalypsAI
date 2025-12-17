package main

import (
    "flag"
    "fmt"
    "net"
    "sync"
    "time"
)

// ScanPorts scans TCP ports on host from start to end inclusive using up to concurrency workers.
// Returns a slice of open ports.
func ScanPorts(host string, start, end, concurrency int) []int {
    if start > end {
        start, end = end, start
    }
    ports := make(chan int, end-start+1)
    results := make(chan int, end-start+1)

    var wg sync.WaitGroup
    // worker function
    worker := func() {
        defer wg.Done()
        for p := range ports {
            address := fmt.Sprintf("%s:%d", host, p)
            conn, err := net.DialTimeout("tcp", address, 200*time.Millisecond)
            if err == nil {
                conn.Close()
                results <- p
            }
        }
    }

    // launch workers
    for i := 0; i < concurrency; i++ {
        wg.Add(1)
        go worker()
    }

    // feed ports
    go func() {
        for p := start; p <= end; p++ {
            ports <- p
        }
        close(ports)
    }()

    // wait for workers then close results
    go func() {
        wg.Wait()
        close(results)
    }()

    var open []int
    for p := range results {
        open = append(open, p)
    }
    return open
}

func main() {
    host := flag.String("host", "localhost", "target host")
    start := flag.Int("start", 1, "starting port")
    end := flag.Int("end", 1024, "ending port")
    conc := flag.Int("c", 100, "concurrency")
    flag.Parse()

    open := ScanPorts(*host, *start, *end, *conc)
    for _, p := range open {
        fmt.Printf("🔎 Port %d is open! The portal hums...\n", p)
    }
}
