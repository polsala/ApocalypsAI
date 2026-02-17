package main

import (
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

type PingResult struct {
    Host    string
    Latency time.Duration
    Err     error
}

// pingHost attempts a TCP connection to the host on port 80 and measures latency.
func pingHost(host string) PingResult {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), 2*time.Second)
    latency := time.Since(start)
    if err == nil {
        conn.Close()
    }
    return PingResult{Host: host, Latency: latency, Err: err}
}

// pingHostsConcurrently pings all hosts using the provided ping function (for testing).
func pingHostsConcurrently(hosts []string, pingFunc func(string) PingResult) []PingResult {
    var wg sync.WaitGroup
    results := make([]PingResult, len(hosts))
    for i, h := range hosts {
        wg.Add(1)
        go func(idx int, host string) {
            defer wg.Done()
            results[idx] = pingFunc(host)
        }(i, h)
    }
    wg.Wait()
    return results
}

// defaultPing is the real implementation used by the CLI.
func defaultPing(host string) PingResult {
    return pingHost(host)
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: nightly-concurrent-ping host1 host2 ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    results := pingHostsConcurrently(hosts, defaultPing)
    for _, r := range results {
        if r.Err != nil {
            fmt.Printf("%s: error (%s)\n", r.Host, r.Err)
        } else {
            fmt.Printf("%s: %d ms\n", r.Host, r.Latency.Milliseconds())
        }
    }
}
