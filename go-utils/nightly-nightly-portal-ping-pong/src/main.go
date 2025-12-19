package main

import (
    "fmt"
    "net"
    "os"
    "sort"
    "sync"
    "time"
)

// latencyFunc is a variable so tests can replace it.
var latencyFunc = measureLatency

// measureLatency attempts to establish a TCP connection to host within timeout.
// Returns the duration it took, or an error if it timed out or failed.
func measureLatency(host string, timeout time.Duration) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", host, timeout)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

type result struct {
    host    string
    latency time.Duration
    err     error
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: portal-ping-pong host1[:port] host2[:port] ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    timeout := 2 * time.Second

    var wg sync.WaitGroup
    resultsCh := make(chan result, len(hosts))

    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            lat, err := latencyFunc(host, timeout)
            resultsCh <- result{host: host, latency: lat, err: err}
        }(h)
    }

    wg.Wait()
    close(resultsCh)

    var results []result
    for r := range resultsCh {
        results = append(results, r)
    }

    // Sort: successful latencies ascending, then failures.
    sort.SliceStable(results, func(i, j int) bool {
        if results[i].err != nil && results[j].err == nil {
            return false
        }
        if results[i].err == nil && results[j].err != nil {
            return true
        }
        return results[i].latency < results[j].latency
    })

    // Print ranking with whimsical emojis.
    emojis := []string{"🏆", "🥈", "🥉"}
    for i, r := range results {
        rank := i + 1
        emoji := ""
        if i < len(emojis) {
            emoji = emojis[i] + " "
        }
        if r.err != nil {
            fmt.Printf("%s%d️⃣ %s – timeout\n", emoji, rank, r.host)
        } else {
            ms := float64(r.latency.Nanoseconds()) / 1e6
            fmt.Printf("%s%d️⃣ %s – %.1fms\n", emoji, rank, r.host, ms)
        }
    }
}
