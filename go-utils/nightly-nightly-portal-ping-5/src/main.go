package main

import (
    "context"
    "errors"
    "flag"
    "fmt"
    "net"
    "os"
    "sort"
    "sync"
    "time"
)

type PingResult struct {
    Host   string
    Latency time.Duration
    Err    error
}

type Pinger func(host string, timeout time.Duration) (time.Duration, error)

// defaultPinger performs a real TCP dial and measures latency.
func defaultPinger(host string, timeout time.Duration) (time.Duration, error) {
    start := time.Now()
    ctx, cancel := context.WithTimeout(context.Background(), timeout)
    defer cancel()
    conn, err := (&net.Dialer{}).DialContext(ctx, "tcp", host)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

func pingHost(host string, timeout time.Duration, pinger Pinger) PingResult {
    latency, err := pinger(host, timeout)
    return PingResult{Host: host, Latency: latency, Err: err}
}

func main() {
    timeoutFlag := flag.Duration("timeout", 2*time.Second, "maximum time to wait for each ping")
    flag.Parse()
    hosts := flag.Args()
    if len(hosts) == 0 {
        fmt.Fprintln(os.Stderr, "Usage: portal-ping [-timeout=2s] host1:port host2:port ...")
        os.Exit(1)
    }

    var wg sync.WaitGroup
    resultsCh := make(chan PingResult, len(hosts))

    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            resultsCh <- pingHost(host, *timeoutFlag, defaultPinger)
        }(h)
    }
    wg.Wait()
    close(resultsCh)

    var results []PingResult
    for r := range resultsCh {
        results = append(results, r)
    }

    // Sort by latency (errors are treated as max duration)
    sort.Slice(results, func(i, j int) bool {
        if results[i].Err != nil && results[j].Err == nil {
            return false
        }
        if results[i].Err == nil && results[j].Err != nil {
            return true
        }
        return results[i].Latency < results[j].Latency
    })

    for _, r := range results {
        if r.Err != nil {
            fmt.Printf("%s\t%s\n", r.Host, "timeout")
        } else {
            fmt.Printf("%s\t%.1fms\n", r.Host, float64(r.Latency.Microseconds())/1000.0)
        }
    }
}
