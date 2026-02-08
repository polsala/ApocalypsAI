package main

import (
    "flag"
    "fmt"
    "net"
    "sort"
    "sync"
    "time"
)

// ScanPorts scans the given ports on host with concurrency workers.
// Returns a slice of open ports sorted ascending.
func ScanPorts(host string, ports []int, workers int) []int {
    var open []int
    var mu sync.Mutex
    jobs := make(chan int, len(ports))
    var wg sync.WaitGroup

    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for p := range jobs {
                address := fmt.Sprintf("%s:%d", host, p)
                conn, err := net.DialTimeout("tcp", address, 200*time.Millisecond)
                if err == nil {
                    conn.Close()
                    mu.Lock()
                    open = append(open, p)
                    mu.Unlock()
                }
            }
        }()
    }

    for _, p := range ports {
        jobs <- p
    }
    close(jobs)
    wg.Wait()
    sort.Ints(open)
    return open
}

func main() {
    host := flag.String("host", "localhost", "target host")
    start := flag.Int("start", 1, "starting port")
    end := flag.Int("end", 1024, "ending port (inclusive)")
    workers := flag.Int("workers", 100, "number of concurrent workers")
    flag.Parse()

    if *start > *end {
        fmt.Println("❗ start port must be <= end port")
        return
    }

    var ports []int
    for p := *start; p <= *end; p++ {
        ports = append(ports, p)
    }

    open := ScanPorts(*host, ports, *workers)
    if len(open) == 0 {
        fmt.Println("🚫 No open ports found.")
        return
    }
    for _, p := range open {
        fmt.Printf("🔓 Port %d is open! 🎉\n", p)
    }
}
