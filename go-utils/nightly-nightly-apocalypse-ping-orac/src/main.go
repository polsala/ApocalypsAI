package main

import (
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

// LatencyProvider returns latency in milliseconds for a given host.
type LatencyProvider func(host string) (int, error)

// defaultProvider measures TCP connection latency to port 80.
func defaultProvider(host string) (int, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), 2*time.Second)
    if err != nil {
        return 0, err
    }
    conn.Close()
    elapsed := time.Since(start)
    return int(elapsed / time.Millisecond), nil
}

// PingHosts concurrently obtains latency for each host using the given provider.
func PingHosts(hosts []string, provider LatencyProvider) map[string]int {
    results := make(map[string]int)
    var mu sync.Mutex
    var wg sync.WaitGroup

    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            latency, err := provider(host)
            if err != nil {
                latency = -1 // indicate failure
            }
            mu.Lock()
            results[host] = latency
            mu.Unlock()
        }(h)
    }
    wg.Wait()
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: ping-oracle <host1> [host2] ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    results := PingHosts(hosts, defaultProvider)
    for _, h := range hosts {
        latency := results[h]
        if latency >= 0 {
            fmt.Printf("%s: %d ms\n", h, latency)
        } else {
            fmt.Printf("%s: unreachable\n", h)
        }
    }
}
