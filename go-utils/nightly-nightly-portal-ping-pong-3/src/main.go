package main

import (
    "errors"
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

type PingFunc func(host string) (time.Duration, error)

var Ping PingFunc = defaultPing

func defaultPing(host string) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), 2*time.Second)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

func pingHost(host string, wg *sync.WaitGroup, ch chan<- PingResult) {
    defer wg.Done()
    latency, err := Ping(host)
    ch <- PingResult{Host: host, Latency: latency, Err: err}
}

func pingConcurrently(hosts []string) []PingResult {
    var wg sync.WaitGroup
    ch := make(chan PingResult, len(hosts))
    for _, h := range hosts {
        wg.Add(1)
        go pingHost(h, &wg, ch)
    }
    wg.Wait()
    close(ch)
    results := make([]PingResult, 0, len(hosts))
    for r := range ch {
        results = append(results, r)
    }
    return results
}

func emojiForLatency(d time.Duration) string {
    if d < 100*time.Millisecond {
        return "🚀"
    } else if d < 300*time.Millisecond {
        return "⚡"
    } else if d < 600*time.Millisecond {
        return "🐢"
    }
    return "💤"
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: portal-ping-pong <host1> <host2> ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    results := pingConcurrently(hosts)
    fmt.Println("🪐 Portal Ping‑Pong Report 🪐")
    for _, r := range results {
        if r.Err != nil {
            fmt.Printf("%s – ❌ %s\n", r.Host, r.Err)
        } else {
            fmt.Printf("%s – %s (%s)\n", r.Host, r.Latency, emojiForLatency(r.Latency))
        }
    }
}
