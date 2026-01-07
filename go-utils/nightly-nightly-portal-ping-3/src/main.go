package main

import (
    "encoding/json"
    "errors"
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

// Result represents the outcome of a single host ping.
type Result struct {
    Host      string `json:"host"`
    LatencyMs int    `json:"latency_ms,omitempty"`
    Error     string `json:"error,omitempty"`
}

// pingFunc abstracts the actual ping operation. It receives a host and a timeout
// and returns the measured latency or an error.
type pingFunc func(host string, timeout time.Duration) (time.Duration, error)

// defaultPing performs a real TCP dial to port 80 and measures the time taken.
func defaultPing(host string, timeout time.Duration) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), timeout)
    if err != nil {
        return 0, err
    }
    _ = conn.Close()
    return time.Since(start), nil
}

// pingHost uses the provided ping implementation and converts the result into a Result struct.
func pingHost(host string, timeout time.Duration, pf pingFunc) Result {
    dur, err := pf(host, timeout)
    if err != nil {
        return Result{Host: host, Error: err.Error()}
    }
    return Result{Host: host, LatencyMs: int(dur.Milliseconds())}
}

// runPings pings a slice of hosts concurrently using a worker pool.
func runPings(hosts []string, maxWorkers int, timeout time.Duration, pf pingFunc) []Result {
    if maxWorkers <= 0 {
        maxWorkers = 1
    }
    var wg sync.WaitGroup
    hostCh := make(chan string)
    resCh := make(chan Result)

    // Start workers.
    for i := 0; i < maxWorkers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for h := range hostCh {
                resCh <- pingHost(h, timeout, pf)
            }
        }()
    }

    // Feed hosts.
    go func() {
        for _, h := range hosts {
            hostCh <- h
        }
        close(hostCh)
    }()

    // Close results channel when workers finish.
    go func() {
        wg.Wait()
        close(resCh)
    }()

    var results []Result
    for r := range resCh {
        results = append(results, r)
    }
    return results
}

func printUsage() {
    fmt.Fprintf(os.Stderr, "Usage: %s <host1> <host2> ...\n", os.Args[0])
    os.Exit(1)
}

func main() {
    if len(os.Args) < 2 {
        printUsage()
    }
    hosts := os.Args[1:]
    const maxWorkers = 10
    const timeout = 5 * time.Second
    results := runPings(hosts, maxWorkers, timeout, defaultPing)
    enc := json.NewEncoder(os.Stdout)
    enc.SetIndent("", "  ")
    if err := enc.Encode(results); err != nil {
        fmt.Fprintf(os.Stderr, "error encoding results: %v\n", err)
        os.Exit(1)
    }
}
