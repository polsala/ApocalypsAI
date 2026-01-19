package main

import (
    "flag"
    "fmt"
    "net"
    "sort"
    "sync"
    "time"
)

// ScanPorts concurrently scans the given ports on host.
// Returns a slice of open ports sorted in ascending order.
func ScanPorts(host string, ports []int, timeout time.Duration, maxConcurrency int) []int {
    var wg sync.WaitGroup
    sem := make(chan struct{}, maxConcurrency)
    results := make(chan int, len(ports))

    for _, port := range ports {
        wg.Add(1)
        sem <- struct{}{}
        go func(p int) {
            defer wg.Done()
            defer func() { <-sem }()
            address := fmt.Sprintf("%s:%d", host, p)
            conn, err := net.DialTimeout("tcp", address, timeout)
            if err == nil {
                conn.Close()
                results <- p
            }
        }(port)
    }

    wg.Wait()
    close(results)

    openPorts := make([]int, 0, len(ports))
    for p := range results {
        openPorts = append(openPorts, p)
    }
    sort.Ints(openPorts)
    return openPorts
}

func main() {
    host := flag.String("host", "", "target hostname or IP (required)")
    start := flag.Int("start", 1, "starting port")
    end := flag.Int("end", 1024, "ending port")
    timeoutStr := flag.String("timeout", "500ms", "connection timeout (e.g., 500ms)")
    workers := flag.Int("workers", 100, "maximum concurrent scans")
    flag.Parse()

    if *host == "" {
        fmt.Println("-host is required")
        flag.Usage()
        return
    }
    if *start < 1 || *end > 65535 || *start > *end {
        fmt.Println("invalid port range")
        return
    }
    timeout, err := time.ParseDuration(*timeoutStr)
    if err != nil {
        fmt.Printf("invalid timeout: %v\n", err)
        return
    }

    ports := make([]int, 0, *end-*start+1)
    for p := *start; p <= *end; p++ {
        ports = append(ports, p)
    }

    open := ScanPorts(*host, ports, timeout, *workers)
    for _, p := range open {
        fmt.Println(p)
    }
}
