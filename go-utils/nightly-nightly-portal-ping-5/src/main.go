package main

import (
    "encoding/json"
    "flag"
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

type Result struct {
    Host       string  `json:"host"`
    Reachable  bool    `json:"reachable"`
    LatencyMs  float64 `json:"latency_ms,omitempty"`
    Error      string  `json:"error,omitempty"`
}

// dialContext is a variable so tests can replace it with a mock.
var dialContext = func(network, address string, timeout time.Duration) (net.Conn, error) {
    return net.DialTimeout(network, address, timeout)
}

func pingHost(host string, timeout time.Duration) Result {
    start := time.Now()
    conn, err := dialContext("tcp", net.JoinHostPort(host, "80"), timeout)
    if err != nil {
        return Result{Host: host, Reachable: false, Error: err.Error()}
    }
    conn.Close()
    latency := time.Since(start).Seconds() * 1000 // ms
    return Result{Host: host, Reachable: true, LatencyMs: latency}
}

func main() {
    timeout := flag.Duration("timeout", 2*time.Second, "connection timeout")
    flag.Parse()
    hosts := flag.Args()
    if len(hosts) == 0 {
        fmt.Fprintln(os.Stderr, "Usage: portal-ping [-timeout=2s] host1 host2 ...")
        os.Exit(1)
    }

    var wg sync.WaitGroup
    results := make([]Result, len(hosts))
    for i, h := range hosts {
        wg.Add(1)
        go func(idx int, host string) {
            defer wg.Done()
            results[idx] = pingHost(host, *timeout)
        }(i, h)
    }
    wg.Wait()

    enc := json.NewEncoder(os.Stdout)
    enc.SetIndent("", "  ")
    if err := enc.Encode(results); err != nil {
        fmt.Fprintln(os.Stderr, "Failed to encode results:", err)
        os.Exit(1)
    }
}
