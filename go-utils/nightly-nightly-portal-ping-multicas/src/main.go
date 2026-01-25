package main

import (
    "context"
    "fmt"
    "net"
    "os"
    "sort"
    "sync"
    "time"
)

type Dialer interface {
    DialContext(ctx context.Context, network, address string) (net.Conn, error)
}

type realDialer struct {
    timeout time.Duration
}

func (d *realDialer) DialContext(ctx context.Context, network, address string) (net.Conn, error) {
    var nd net.Dialer
    nd.Timeout = d.timeout
    return nd.DialContext(ctx, network, address)
}

type PingResult struct {
    Host    string
    Open    bool
    Latency time.Duration
}

func pingHost(d Dialer, address string) PingResult {
    start := time.Now()
    ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
    defer cancel()
    conn, err := d.DialContext(ctx, "tcp", address)
    elapsed := time.Since(start)
    if err != nil {
        return PingResult{Host: address, Open: false}
    }
    conn.Close()
    return PingResult{Host: address, Open: true, Latency: elapsed}
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: portal-ping host:port [host:port ...]")
        os.Exit(1)
    }
    hosts := os.Args[1:]

    d := &realDialer{timeout: 2 * time.Second}
    var wg sync.WaitGroup
    resultsCh := make(chan PingResult, len(hosts))

    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            resultsCh <- pingHost(d, host)
        }(h)
    }
    wg.Wait()
    close(resultsCh)

    var results []PingResult
    for r := range resultsCh {
        results = append(results, r)
    }

    // sort open hosts by latency, keep closed at the end
    sort.Slice(results, func(i, j int) bool {
        if results[i].Open && results[j].Open {
            return results[i].Latency < results[j].Latency
        }
        return results[i].Open && !results[j].Open
    })

    fmt.Printf("%-25s %-6s %s\n", "Host", "Status", "Latency")
    for _, r := range results {
        status := "closed"
        latency := "-"
        if r.Open {
            status = "open"
            latency = fmt.Sprintf("%dms", r.Latency.Milliseconds())
        }
        fmt.Printf("%-25s %-6s %s\n", r.Host, status, latency)
    }
}
