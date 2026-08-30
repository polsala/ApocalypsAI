package main

import (
    "encoding/json"
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

type Result struct {
    Host      string  `json:"host"`
    LatencyMs float64 `json:"latency_ms,omitempty"`
    Error     string  `json:"error,omitempty"`
}

// PingHost attempts a TCP connection to the given host within the timeout.
// On success it returns the elapsed time in milliseconds; on failure it returns the error string.
func PingHost(host string, timeout time.Duration) Result {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", host, timeout)
    if err != nil {
        return Result{Host: host, Error: err.Error()}
    }
    conn.Close()
    elapsed := time.Since(start).Seconds() * 1000
    return Result{Host: host, LatencyMs: elapsed}
}

// PingHosts concurrently pings a slice of hosts respecting the concurrency limit.
func PingHosts(hosts []string, timeout time.Duration, concurrency int) []Result {
    var wg sync.WaitGroup
    sem := make(chan struct{}, concurrency)
    results := make([]Result, len(hosts))
    for i, h := range hosts {
        wg.Add(1)
        go func(idx int, host string) {
            defer wg.Done()
            sem <- struct{}{}
            results[idx] = PingHost(host, timeout)
            <-sem
        }(i, h)
    }
    wg.Wait()
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: go run ./src/main.go host1:port [host2:port ...]")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    timeout := 2 * time.Second
    concurrency := 10
    res := PingHosts(hosts, timeout, concurrency)
    out, _ := json.MarshalIndent(res, "", "  ")
    fmt.Println(string(out))
}
