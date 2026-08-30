package main

import (
    "flag"
    "fmt"
    "net"
    "strconv"
    "strings"
    "sync"
    "time"
)

type Result struct {
    Port int
    Open bool
}

// parsePortRange converts a string like "8000-8010" into a slice of ints.
func parsePortRange(r string) ([]int, error) {
    parts := strings.Split(r, "-")
    if len(parts) != 2 {
        return nil, fmt.Errorf("invalid port range: %s", r)
    }
    start, err := strconv.Atoi(strings.TrimSpace(parts[0]))
    if err != nil {
        return nil, err
    }
    end, err := strconv.Atoi(strings.TrimSpace(parts[1]))
    if err != nil {
        return nil, err
    }
    if start > end || start < 1 || end > 65535 {
        return nil, fmt.Errorf("invalid port numbers: %d-%d", start, end)
    }
    ports := make([]int, 0, end-start+1)
    for p := start; p <= end; p++ {
        ports = append(ports, p)
    }
    return ports, nil
}

// scanPort attempts to connect to host:port with a short timeout.
func scanPort(host string, port int, timeout time.Duration) bool {
    address := fmt.Sprintf("%s:%d", host, port)
    conn, err := net.DialTimeout("tcp", address, timeout)
    if err != nil {
        return false
    }
    conn.Close()
    return true
}

// ScanPorts performs a concurrent scan over the provided ports.
func ScanPorts(host string, ports []int, workers int, timeout time.Duration) []Result {
    jobs := make(chan int, len(ports))
    results := make([]Result, len(ports))
    var wg sync.WaitGroup
    var mu sync.Mutex

    // launch workers
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for port := range jobs {
                open := scanPort(host, port, timeout)
                mu.Lock()
                results[port-ports[0]] = Result{Port: port, Open: open}
                mu.Unlock()
            }
        }()
    }

    // feed jobs
    for _, p := range ports {
        jobs <- p
    }
    close(jobs)
    wg.Wait()
    return results
}

func main() {
    hostPtr := flag.String("host", "localhost", "target hostname or IP")
    portsPtr := flag.String("ports", "1-1024", "port range in the form start-end")
    workersPtr := flag.Int("workers", 100, "number of concurrent workers")
    timeoutPtr := flag.Duration("timeout", 200*time.Millisecond, "dial timeout per port")
    flag.Parse()

    ports, err := parsePortRange(*portsPtr)
    if err != nil {
        fmt.Printf("❌ Error parsing ports: %v\n", err)
        return
    }

    fmt.Printf("🔍 Scanning %s ports %s-%s with %d workers...\n", *hostPtr, strconv.Itoa(ports[0]), strconv.Itoa(ports[len(ports)-1]), *workersPtr)
    results := ScanPorts(*hostPtr, ports, *workersPtr, *timeoutPtr)
    for _, r := range results {
        if r.Open {
            fmt.Printf("✨ Port %d is open! The portal welcomes you.\n", r.Port)
        } else {
            fmt.Printf("❌ Port %d is closed.\n", r.Port)
        }
    }
}
