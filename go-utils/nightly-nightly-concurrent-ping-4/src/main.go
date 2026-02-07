package main

import (
    "encoding/json"
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

// pingResult holds either a latency in milliseconds or an error string.
type pingResult struct {
    LatencyMs int64  `json:"latency_ms,omitempty"`
    Error     string `json:"error,omitempty"`
}

// dialFunc abstracts net.DialTimeout for easier testing.
type dialFunc func(network, address string, timeout time.Duration) (net.Conn, error)

// pingHost attempts a TCP connection to the given host on port 80 using the supplied dialer.
// It returns the elapsed time in milliseconds or an error.
func pingHost(host string, timeout time.Duration, dialer dialFunc) (int64, error) {
    start := time.Now()
    conn, err := dialer("tcp", net.JoinHostPort(host, "80"), timeout)
    if err != nil {
        return 0, err
    }
    // Successful connection – close immediately.
    conn.Close()
    elapsed := time.Since(start).Milliseconds()
    return elapsed, nil
}

// defaultDialer is the production implementation using net.DialTimeout.
func defaultDialer(network, address string, timeout time.Duration) (net.Conn, error) {
    return net.DialTimeout(network, address, timeout)
}

// concurrentPing pings all hosts concurrently and returns a map of host -> pingResult.
func concurrentPing(hosts []string, timeout time.Duration, dialer dialFunc) map[string]pingResult {
    var wg sync.WaitGroup
    results := make(map[string]pingResult)
    mu := sync.Mutex{}

    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            latency, err := pingHost(host, timeout, dialer)
            mu.Lock()
            defer mu.Unlock()
            if err != nil {
                results[host] = pingResult{Error: err.Error()}
            } else {
                results[host] = pingResult{LatencyMs: latency}
            }
        }(h)
    }
    wg.Wait()
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Fprintf(os.Stderr, "Usage: %s host1 [host2 ...]\n", os.Args[0])
        os.Exit(1)
    }
    hosts := os.Args[1:]
    timeout := 3 * time.Second
    results := concurrentPing(hosts, timeout, defaultDialer)

    // Convert to a simple map[string]interface{} for pretty JSON output.
    out := make(map[string]interface{})
    for h, r := range results {
        if r.Error != "" {
            out[h] = r.Error
        } else {
            out[h] = r.LatencyMs
        }
    }
    enc := json.NewEncoder(os.Stdout)
    enc.SetIndent("", "  ")
    if err := enc.Encode(out); err != nil {
        fmt.Fprintf(os.Stderr, "Failed to encode JSON: %v\n", err)
        os.Exit(1)
    }
}
