package main

import (
    "encoding/json"
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

type PingResult struct {
    Host    string        `json:"host"`
    Latency time.Duration `json:"latency_ms,omitempty"`
    Error   string        `json:"error,omitempty"`
}

// PingFunc defines a function that pings a host and returns latency.
type PingFunc func(host string) (time.Duration, error)

// realPing performs a TCP connect to host:80 with a timeout and measures latency.
func realPing(host string) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), 2*time.Second)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

// PingHosts pings all hosts concurrently using the provided ping function.
func PingHosts(hosts []string, pingFn PingFunc) []PingResult {
    var wg sync.WaitGroup
    results := make([]PingResult, len(hosts))
    for i, h := range hosts {
        wg.Add(1)
        go func(idx int, host string) {
            defer wg.Done()
            latency, err := pingFn(host)
            if err != nil {
                results[idx] = PingResult{Host: host, Error: err.Error()}
            } else {
                results[idx] = PingResult{Host: host, Latency: latency}
            }
        }(i, h)
    }
    wg.Wait()
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: ping-aggregator <host1> <host2> ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    results := PingHosts(hosts, realPing)
    out, err := json.MarshalIndent(results, "", "  ")
    if err != nil {
        fmt.Fprintf(os.Stderr, "error marshaling results: %v\n", err)
        os.Exit(1)
    }
    fmt.Println(string(out))
}
