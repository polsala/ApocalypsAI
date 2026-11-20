package main

import (
    "flag"
    "fmt"
    "net"
    "sync"
    "time"
)

// ScanPorts scans TCP ports on the given host from start to end (inclusive).
// It returns a slice of open ports. The scan is performed with a worker pool
// limited by the workers argument.
func ScanPorts(host string, start, end int, timeout time.Duration, workers int) []int {
    var open []int
    var mu sync.Mutex
    ports := make(chan int, workers)
    var wg sync.WaitGroup

    // launch workers
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for p := range ports {
                address := fmt.Sprintf("%s:%d", host, p)
                conn, err := net.DialTimeout("tcp", address, timeout)
                if err == nil {
                    conn.Close()
                    mu.Lock()
                    open = append(open, p)
                    mu.Unlock()
                }
            }
        }()
    }

    // feed ports to workers
    for p := start; p <= end; p++ {
        ports <- p
    }
    close(ports)
    wg.Wait()
    return open
}

func main() {
    host := flag.String("host", "", "target hostname or IP")
    start := flag.Int("start", 1, "starting port")
    end := flag.Int("end", 1024, "ending port")
    timeout := flag.Duration("timeout", 500*time.Millisecond, "connection timeout")
    workers := flag.Int("workers", 100, "number of concurrent workers")
    flag.Parse()

    if *host == "" {
        fmt.Println("error: -host is required")
        flag.Usage()
        return
    }

    openPorts := ScanPorts(*host, *start, *end, *timeout, *workers)
    for _, p := range openPorts {
        fmt.Printf("⚡️ Port %d is open! (Gateway to the wasteland)\n", p)
    }
    if len(openPorts) == 0 {
        fmt.Println("No open ports found. The wasteland is silent.")
    }
}
