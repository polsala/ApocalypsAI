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

// ScanPorts concurrently checks a list of TCP ports on the given host.
// It returns a slice of ports that responded within the timeout.
func ScanPorts(host string, ports []int, timeout time.Duration) []int {
    var wg sync.WaitGroup
    // semaphore to limit concurrent connections (avoid exhausting resources)
    sem := make(chan struct{}, 100)
    results := make(chan int, len(ports))

    for _, p := range ports {
        wg.Add(1)
        go func(port int) {
            defer wg.Done()
            sem <- struct{}{}
            defer func() { <-sem }()
            address := net.JoinHostPort(host, strconv.Itoa(port))
            conn, err := net.DialTimeout("tcp", address, timeout)
            if err == nil {
                conn.Close()
                results <- port
            }
        }(p)
    }

    wg.Wait()
    close(results)

    openPorts := make([]int, 0, len(ports))
    for p := range results {
        openPorts = append(openPorts, p)
    }
    return openPorts
}

func parsePorts(portStr string) ([]int, error) {
    parts := strings.Split(portStr, ",")
    ports := make([]int, 0, len(parts))
    for _, part := range parts {
        p, err := strconv.Atoi(strings.TrimSpace(part))
        if err != nil {
            return nil, fmt.Errorf("invalid port %q: %w", part, err)
        }
        ports = append(ports, p)
    }
    return ports, nil
}

func main() {
    host := flag.String("host", "localhost", "target host to scan")
    portsStr := flag.String("ports", "", "comma‑separated list of ports to scan (e.g., 80,443,8080)")
    timeoutMs := flag.Int("timeout", 500, "dial timeout in milliseconds")
    flag.Parse()

    if *portsStr == "" {
        fmt.Println("error: -ports flag is required")
        return
    }

    ports, err := parsePorts(*portsStr)
    if err != nil {
        fmt.Printf("error parsing ports: %v\n", err)
        return
    }

    open := ScanPorts(*host, ports, time.Duration(*timeoutMs)*time.Millisecond)
    if len(open) == 0 {
        fmt.Printf("No open ports on %s\n", *host)
        return
    }
    fmt.Printf("Open ports on %s: ", *host)
    for i, p := range open {
        if i > 0 {
            fmt.Print(" ")
        }
        fmt.Print(p)
    }
    fmt.Println()
}
