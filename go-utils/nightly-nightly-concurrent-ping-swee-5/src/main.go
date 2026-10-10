package main

import (
    "fmt"
    "net"
    "os"
    "sort"
    "sync"
    "time"
)

type pingResult struct {
    Host    string
    Latency time.Duration
    Err     error
}

// dialerFunc abstracts the network call for easier testing.
var dialerFunc = realDial

// realDial attempts a TCP connection to host:80 with a 2‑second timeout and returns the elapsed time.
func realDial(host string) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), 2*time.Second)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

// pingHost uses dialerFunc to measure latency for a single host.
func pingHost(host string) pingResult {
    latency, err := dialerFunc(host)
    return pingResult{Host: host, Latency: latency, Err: err}
}

// pingHosts concurrently pings all provided hosts and returns results sorted by latency (fastest first).
func pingHosts(hosts []string) []pingResult {
    var wg sync.WaitGroup
    resultsCh := make(chan pingResult, len(hosts))

    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            resultsCh <- pingHost(host)
        }(h)
    }

    wg.Wait()
    close(resultsCh)

    var results []pingResult
    for r := range resultsCh {
        results = append(results, r)
    }

    // Sort: successful pings first, ordered by latency; errors after.
    sort.SliceStable(results, func(i, j int) bool {
        if results[i].Err != nil && results[j].Err == nil {
            return false
        }
        if results[i].Err == nil && results[j].Err != nil {
            return true
        }
        if results[i].Err != nil && results[j].Err != nil {
            return results[i].Host < results[j].Host
        }
        return results[i].Latency < results[j].Latency
    })
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: ping-sweeper <host1> <host2> ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    results := pingHosts(hosts)
    for _, r := range results {
        if r.Err != nil {
            fmt.Printf("%s\terror: %v\n", r.Host, r.Err)
        } else {
            fmt.Printf("%s\t%v\n", r.Host, r.Latency)
        }
    }
}
