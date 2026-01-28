package main

import (
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

// PingResult holds the outcome of a ping.
type PingResult struct {
    Host    string
    Latency time.Duration
    Err     error
}

// PingFunc defines the signature for a ping operation.
// It can be swapped out in tests.
var PingFunc = defaultPing

// defaultPing performs a TCP dial to the host on port 80 with the given timeout.
func defaultPing(host string, timeout time.Duration) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), timeout)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

// pingAll pings each host concurrently and returns a slice of results.
func pingAll(hosts []string, timeout time.Duration) []PingResult {
    var wg sync.WaitGroup
    results := make([]PingResult, len(hosts))
    for i, h := range hosts {
        wg.Add(1)
        go func(idx int, host string) {
            defer wg.Done()
            latency, err := PingFunc(host, timeout)
            results[idx] = PingResult{Host: host, Latency: latency, Err: err}
        }(i, h)
    }
    wg.Wait()
    return results
}

// formatResult creates a human‑readable line for a PingResult.
func formatResult(r PingResult) string {
    if r.Err != nil {
        return fmt.Sprintf("%s: %s", r.Host, r.Err.Error())
    }
    return fmt.Sprintf("%s: %dms", r.Host, r.Latency.Milliseconds())
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: portal-ping <host1> [host2] ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    timeout := 2 * time.Second
    results := pingAll(hosts, timeout)
    for _, r := range results {
        fmt.Println(formatResult(r))
    }
}
