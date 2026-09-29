package main

import (
    "encoding/json"
    "fmt"
    "os"
    "sync"
)

type Result struct {
    Host      string `json:"host"`
    LatencyMs int    `json:"latency_ms"`
}

// computeLatency returns a deterministic fake latency (1‑100 ms) for a host.
// It sums the byte values of the hostname, takes modulo 100, and adds 1.
func computeLatency(host string) int {
    sum := 0
    for _, b := range []byte(host) {
        sum += int(b)
    }
    return (sum % 100) + 1
}

// pingHosts concurrently computes latencies for a slice of hosts.
func pingHosts(hosts []string) []Result {
    var wg sync.WaitGroup
    results := make([]Result, len(hosts))
    for i, h := range hosts {
        wg.Add(1)
        go func(idx int, host string) {
            defer wg.Done()
            latency := computeLatency(host)
            results[idx] = Result{Host: host, LatencyMs: latency}
        }(i, h)
    }
    wg.Wait()
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Fprintf(os.Stderr, "Usage: %s <host1> [<host2> ...]\n", os.Args[0])
        os.Exit(1)
    }
    hosts := os.Args[1:]
    results := pingHosts(hosts)
    enc := json.NewEncoder(os.Stdout)
    enc.SetIndent("", "  ")
    if err := enc.Encode(results); err != nil {
        fmt.Fprintf(os.Stderr, "Error encoding JSON: %v\n", err)
        os.Exit(1)
    }
}
