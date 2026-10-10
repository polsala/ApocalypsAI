package main

import (
    "flag"
    "fmt"
    "net"
    "sort"
    "sync"
    "time"
)

// scanPort attempts to establish a TCP connection to host:port within the given timeout.
// It returns true if the connection succeeds (port is open).
func scanPort(host string, port int, timeout time.Duration) bool {
    address := fmt.Sprintf("%s:%d", host, port)
    conn, err := net.DialTimeout("tcp", address, timeout)
    if err != nil {
        return false
    }
    conn.Close()
    return true
}

// ScanPorts concurrently scans the supplied slice of ports on the given host.
// concurrency limits the number of simultaneous goroutines.
// It returns a sorted slice of open ports.
func ScanPorts(host string, ports []int, concurrency int, timeout time.Duration) []int {
    var wg sync.WaitGroup
    sem := make(chan struct{}, concurrency)
    results := make(chan int, len(ports))

    for _, p := range ports {
        wg.Add(1)
        go func(port int) {
            defer wg.Done()
            sem <- struct{}{}
            defer func() { <-sem }()
            if scanPort(host, port, timeout) {
                results <- port
            }
        }(p)
    }

    wg.Wait()
    close(results)

    var open []int
    for p := range results {
        open = append(open, p)
    }
    sort.Ints(open)
    return open
}

func main() {
    host := flag.String("host", "localhost", "Target host or IP address")
    start := flag.Int("start", 1, "Starting port (inclusive)")
    end := flag.Int("end", 1024, "Ending port (inclusive)")
    concurrency := flag.Int("concurrency", 100, "Maximum concurrent workers")
    timeoutMs := flag.Int("timeout", 200, "Connection timeout in milliseconds")
    flag.Parse()

    if *start < 1 || *end > 65535 || *start > *end {
        fmt.Println("Invalid port range. Ports must be between 1 and 65535 and start <= end.")
        return
    }

    var ports []int
    for p := *start; p <= *end; p++ {
        ports = append(ports, p)
    }

    timeout := time.Duration(*timeoutMs) * time.Millisecond
    fmt.Printf("Scanning %d‑%d on %s with up to %d workers…\n", *start, *end, *host, *concurrency)
    openPorts := ScanPorts(*host, ports, *concurrency, timeout)

    for _, p := range openPorts {
        fmt.Printf("🔥 Port %d is open!\n", p)
    }
    fmt.Printf("Scanning complete. %d open port(s) found.\n", len(openPorts))
}
