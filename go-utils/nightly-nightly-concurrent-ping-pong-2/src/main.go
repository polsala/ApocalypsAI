package main

import (
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

type pingResult struct {
    Host      string
    LatencyMs int
    Err       error
}

// pingFunc is a variable so tests can inject a mock implementation.
var pingFunc = realPing

func realPing(host string) (int, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), 2*time.Second)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return int(time.Since(start).Milliseconds()), nil
}

func pingHost(host string, wg *sync.WaitGroup, ch chan<- pingResult) {
    defer wg.Done()
    latency, err := pingFunc(host)
    ch <- pingResult{Host: host, LatencyMs: latency, Err: err}
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: pingpong <host1> [host2] ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    var wg sync.WaitGroup
    resultsCh := make(chan pingResult, len(hosts))

    for _, h := range hosts {
        wg.Add(1)
        go pingHost(h, &wg, resultsCh)
    }
    wg.Wait()
    close(resultsCh)

    fmt.Println("🔔 Ping Pong Report 🔔")
    for r := range resultsCh {
        if r.Err != nil {
            fmt.Printf("❌ %s: unreachable (%s)\n", r.Host, r.Err)
        } else {
            fmt.Printf("✅ %s: %d ms\n", r.Host, r.LatencyMs)
        }
    }
}
