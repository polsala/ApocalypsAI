package main

import (
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

type pingResult struct {
    host    string
    latency time.Duration
    err     error
}

// pingFunc is a variable that can be swapped out in tests.
var pingFunc = realPing

func realPing(host string) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), 2*time.Second)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

func categorize(latency time.Duration) string {
    ms := latency.Milliseconds()
    switch {
    case ms < 50:
        return "🐇 Lightning rabbit"
    case ms < 150:
        return "🐦 Swift sparrow"
    case ms < 300:
        return "🐢 Steady turtle"
    default:
        return "🐌 Slothful snail"
    }
}

func pingHost(host string, wg *sync.WaitGroup, out chan<- pingResult) {
    defer wg.Done()
    d, err := pingFunc(host)
    out <- pingResult{host: host, latency: d, err: err}
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: pingpong <host1> [host2] ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    var wg sync.WaitGroup
    results := make(chan pingResult, len(hosts))

    for _, h := range hosts {
        wg.Add(1)
        go pingHost(h, &wg, results)
    }
    wg.Wait()
    close(results)

    for r := range results {
        if r.err != nil {
            fmt.Printf("%s: ❌ error (%s)\n", r.host, r.err)
            continue
        }
        fmt.Printf("%s: %s (%d ms)\n", r.host, categorize(r.latency), r.latency.Milliseconds())
    }
}
