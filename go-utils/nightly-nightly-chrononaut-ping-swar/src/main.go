package main

import (
    "errors"
    "fmt"
    "net"
    "os"
    "sort"
    "sync"
    "time"
)

type PingResult struct {
    Host    string
    Latency time.Duration
    Err     error
}

// pingFunc is a variable so tests can replace it with a mock implementation.
var pingFunc = realPing

// realPing performs a TCP connection to the host on port 80 and measures latency.
func realPing(host string) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), 2*time.Second)
    if err != nil {
        return 0, err
    }
    _ = conn.Close()
    return time.Since(start), nil
}

// RunPingSwarm pings all hosts concurrently and returns a slice of results.
func RunPingSwarm(hosts []string) ([]PingResult, error) {
    if len(hosts) == 0 {
        return nil, errors.New("no hosts provided")
    }
    results := make([]PingResult, len(hosts))
    var wg sync.WaitGroup
    wg.Add(len(hosts))
    for i, h := range hosts {
        go func(idx int, host string) {
            defer wg.Done()
            latency, err := pingFunc(host)
            results[idx] = PingResult{Host: host, Latency: latency, Err: err}
        }(i, h)
    }
    wg.Wait()
    // Sort by latency, placing errors at the end.
    sort.SliceStable(results, func(i, j int) bool {
        if results[i].Err != nil && results[j].Err == nil {
            return false
        }
        if results[i].Err == nil && results[j].Err != nil {
            return true
        }
        return results[i].Latency < results[j].Latency
    })
    return results, nil
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: ping-swarm <host1> <host2> ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    results, err := RunPingSwarm(hosts)
    if err != nil {
        fmt.Fprintf(os.Stderr, "Error: %v\n", err)
        os.Exit(1)
    }
    fmt.Printf("Host\t\tLatency\tStatus\n")
    fmt.Printf("------------------------------------------\n")
    for _, r := range results {
        if r.Err != nil {
            fmt.Printf("%s\t-\tERROR: %v\n", r.Host, r.Err)
        } else {
            fmt.Printf("%s\t%v\tOK\n", r.Host, r.Latency)
        }
    }
}
