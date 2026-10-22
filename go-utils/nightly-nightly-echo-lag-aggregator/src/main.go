package main

import (
    "fmt"
    "net"
    "os"
    "sort"
    "strings"
    "sync"
    "time"
)

type result struct {
    host    string
    latency time.Duration
    err     error
}

// measureLatency is a variable so tests can replace it with a mock.
var measureLatency = func(host string) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), 2*time.Second)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

func aggregate(hosts []string) []result {
    var wg sync.WaitGroup
    resCh := make(chan result, len(hosts))
    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            lat, err := measureLatency(host)
            resCh <- result{host: host, latency: lat, err: err}
        }(h)
    }
    wg.Wait()
    close(resCh)
    results := make([]result, 0, len(hosts))
    for r := range resCh {
        results = append(results, r)
    }
    sort.Slice(results, func(i, j int) bool {
        // Treat errors as infinite latency so they appear last.
        if results[i].err != nil {
            return false
        }
        if results[j].err != nil {
            return true
        }
        return results[i].latency < results[j].latency
    })
    return results
}

func formatBar(d time.Duration) string {
    // One block per 10ms, minimum one block for non‑zero latency.
    ms := d.Milliseconds()
    blocks := int(ms / 10)
    if blocks < 1 && ms > 0 {
        blocks = 1
    }
    return strings.Repeat("█", blocks)
}

func formatResult(r result) string {
    if r.err != nil {
        return fmt.Sprintf("%s   error: %v", r.host, r.err)
    }
    ms := r.latency.Milliseconds()
    bar := formatBar(r.latency)
    return fmt.Sprintf("%s   %dms  %s", r.host, ms, bar)
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: go run ./src/main.go <host1> <host2> ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    results := aggregate(hosts)
    for _, r := range results {
        fmt.Println(formatResult(r))
    }
}
