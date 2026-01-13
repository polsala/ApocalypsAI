package main

import (
    "fmt"
    "net"
    "os"
    "strings"
    "sync"
    "time"
)

type result struct {
    host    string
    latency time.Duration
    err     error
}

// pingHost attempts a TCP connection to the given address (host[:port])
// using the provided timeout and returns the latency.
func pingHost(address string, timeout time.Duration) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", address, timeout)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

// PingHosts concurrently pings a slice of hosts and returns a map of host to latency.
// If a host cannot be reached, the latency will be zero and the error recorded.
func PingHosts(hosts []string, timeout time.Duration) map[string]result {
    results := make(map[string]result)
    var wg sync.WaitGroup
    mu := sync.Mutex{}
    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            // If no port is specified, default to 80.
            address := host
            if !strings.Contains(host, ":") {
                address = fmt.Sprintf("%s:80", host)
            }
            lat, err := pingHost(address, timeout)
            mu.Lock()
            results[host] = result{host: host, latency: lat, err: err}
            mu.Unlock()
        }(h)
    }
    wg.Wait()
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: portal-ping host1 [host2 ...]")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    timeout := 5 * time.Second
    res := PingHosts(hosts, timeout)
    fmt.Printf("âââââââââââââââââââââââ¬ââââââââââââââââ\n")
    fmt.Printf("â Host                â Latency (ms)  â\n")
    fmt.Printf("âââââââââââââââââââââââ¼ââââââââââââââââ¤\n")
    for _, h := range hosts {
        r := res[h]
        if r.err != nil {
            fmt.Printf("â %-20s â error         â\n", h)
        } else {
            fmt.Printf("â %-20s â %-13d â\n", h, r.latency.Milliseconds())
        }
    }
    fmt.Printf("âââââââââââââââââââââââ´ââââââââââââââââ\n")
}

