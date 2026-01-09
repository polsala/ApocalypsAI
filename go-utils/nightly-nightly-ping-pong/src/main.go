package main

import (
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

// pingHost attempts a TCP connection to host:80 with the given timeout.
// It returns the elapsed time or an error if the connection fails.
func pingHost(host string, timeout time.Duration) (time.Duration, error) {
    address := net.JoinHostPort(host, "80")
    start := time.Now()
    conn, err := net.DialTimeout("tcp", address, timeout)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

// pingHosts concurrently pings all hosts and returns a map of host -> latency.
func pingHosts(hosts []string, timeout time.Duration) map[string]time.Duration {
    results := make(map[string]time.Duration)
    var mu sync.Mutex
    var wg sync.WaitGroup
    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            if dur, err := pingHost(host, timeout); err == nil {
                mu.Lock()
                results[host] = dur
                mu.Unlock()
            } else {
                mu.Lock()
                results[host] = -1
                mu.Unlock()
            }
        }(h)
    }
    wg.Wait()
    return results
}

// verdict returns a whimsical speed description based on latency.
func verdict(d time.Duration) string {
    if d < 0 {
        return "Unreachable"
    }
    ms := d.Milliseconds()
    switch {
    case ms < 50:
        return "⚡ Lightning fast"
    case ms < 150:
        return "🚀 Supersonic"
    case ms < 300:
        return "🏎️ Quick"
    case ms < 600:
        return "🐢 Moderate"
    default:
        return "🦥 Snail pace"
    }
}

func main() {
    hosts := os.Args[1:]
    if len(hosts) == 0 {
        hosts = []string{"google.com", "github.com", "example.com"}
    }
    timeout := 2 * time.Second
    fmt.Printf("Pinging %d host(s) with a %v timeout...\n\n", len(hosts), timeout)
    results := pingHosts(hosts, timeout)
    for _, h := range hosts {
        dur := results[h]
        fmt.Printf("%s: ", h)
        if dur < 0 {
            fmt.Printf("%s\n", verdict(dur))
        } else {
            fmt.Printf("%d ms – %s\n", dur.Milliseconds(), verdict(dur))
        }
    }
}
