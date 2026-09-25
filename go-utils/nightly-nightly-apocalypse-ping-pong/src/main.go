package main

import (
    "fmt"
    "net"
    "os"
    "sort"
    "sync"
    "time"
)

type HostResult struct {
    Host    string
    Latency time.Duration
    Err     error
}

// pingFunc is a variable so tests can replace it with a mock.
var pingFunc = pingHost

func pingHost(host string) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), 2*time.Second)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

func emojiForLatency(d time.Duration) string {
    ms := d.Milliseconds()
    switch {
    case ms < 50:
        return "⚡"
    case ms < 200:
        return "~"
    default:
        return "🐢"
    }
}

func generateReport(hosts []string) string {
    var wg sync.WaitGroup
    results := make([]HostResult, len(hosts))
    for i, h := range hosts {
        wg.Add(1)
        go func(idx int, host string) {
            defer wg.Done()
            lat, err := pingFunc(host)
            results[idx] = HostResult{Host: host, Latency: lat, Err: err}
        }(i, h)
    }
    wg.Wait()

    // sort by latency, putting errors at the end
    sort.Slice(results, func(i, j int) bool {
        if results[i].Err != nil {
            return false
        }
        if results[j].Err != nil {
            return true
        }
        return results[i].Latency < results[j].Latency
    })

    var out string
    for _, r := range results {
        if r.Err != nil {
            out += fmt.Sprintf("❌ %s (error: %s)\n", r.Host, r.Err)
            continue
        }
        out += fmt.Sprintf("%s %s (%dms)\n", emojiForLatency(r.Latency), r.Host, r.Latency.Milliseconds())
    }
    return out
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: pingpong <host1> <host2> ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    report := generateReport(hosts)
    fmt.Print(report)
}
