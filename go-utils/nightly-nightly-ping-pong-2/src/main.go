package main

import (
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

// pingFunc abstracts the network call for easier testing.
type pingFunc func(host string) (time.Duration, error)

// defaultPing performs a TCP dial with a 2s timeout.
func defaultPing(host string) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", host, 2*time.Second)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

// ping is the function used by the program; it can be swapped in tests.
var ping pingFunc = defaultPing

// runPings concurrently pings each host and returns a slice of results.
func runPings(hosts []string) []PingResult {
    var wg sync.WaitGroup
    results := make([]PingResult, len(hosts))
    for i, h := range hosts {
        wg.Add(1)
        go func(idx int, host string) {
            defer wg.Done()
            latency, err := ping(host)
            results[idx] = PingResult{Host: host, Latency: latency, Err: err}
        }(i, h)
    }
    wg.Wait()
    return results
}

// emojiForLatency returns a whimsical emoji based on latency.
func emojiForLatency(d time.Duration) string {
    if d < 50*time.Millisecond {
        return "🚀"
    }
    if d < 150*time.Millisecond {
        return "🌟"
    }
    return "🐢"
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: go run src/main.go host1:port [host2:port ...]")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    results := runPings(hosts)

    var total time.Duration
    var count int
    for _, r := range results {
        if r.Err != nil {
            fmt.Printf("%s → timeout ⏱️\n", r.Host)
            continue
        }
        fmt.Printf("%s → %dms %s\n", r.Host, r.Latency.Milliseconds(), emojiForLatency(r.Latency))
        total += r.Latency
        count++
    }
    if count > 0 {
        avg := total / time.Duration(count)
        fmt.Printf("Average latency: %dms 🎉\n", avg.Milliseconds())
    }
}
