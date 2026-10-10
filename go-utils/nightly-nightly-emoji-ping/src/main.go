package main

import (
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

// pingFunc is a variable so tests can replace it with a mock implementation.
var pingFunc = pingHost

// pingHost attempts a TCP connection to the host on port 80 with the given timeout.
// It returns the latency or an error if the host is unreachable.
func pingHost(host string, timeout time.Duration) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), timeout)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

// emojiForLatency returns an emoji based on the measured latency.
func emojiForLatency(latency time.Duration) string {
    switch {
    case latency < 50*time.Millisecond:
        return "🚀"
    case latency < 150*time.Millisecond:
        return "⚡"
    default:
        return "🐢"
    }
}

// formatResult builds the human‑readable output line for a host.
func formatResult(host string, latency time.Duration, err error) string {
    if err != nil {
        return fmt.Sprintf("%s: down ❌", host)
    }
    emoji := emojiForLatency(latency)
    return fmt.Sprintf("%s: up (%dms) %s", host, latency.Milliseconds(), emoji)
}

// runPings pings all hosts concurrently and returns a slice of formatted results.
func runPings(hosts []string, timeout time.Duration) []string {
    var wg sync.WaitGroup
    results := make([]string, len(hosts))
    for i, host := range hosts {
        wg.Add(1)
        go func(idx int, h string) {
            defer wg.Done()
            latency, err := pingFunc(h, timeout)
            results[idx] = formatResult(h, latency, err)
        }(i, host)
    }
    wg.Wait()
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: emoji-ping <host1> [host2] ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    timeout := 2 * time.Second
    outputs := runPings(hosts, timeout)
    for _, line := range outputs {
        fmt.Println(line)
    }
}
