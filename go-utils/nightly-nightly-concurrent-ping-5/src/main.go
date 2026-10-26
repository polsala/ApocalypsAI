package main

import (
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

type PingProvider interface {
    Ping(host string) (time.Duration, error)
}

type RealPingProvider struct{}

func (p RealPingProvider) Ping(host string) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), 2*time.Second)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

// PingHosts pings each host concurrently using the supplied provider.
// It returns a map of host -> latency. Unreachable hosts get a latency of -1.
func PingHosts(provider PingProvider, hosts []string) map[string]time.Duration {
    results := make(map[string]time.Duration)
    var mu sync.Mutex
    var wg sync.WaitGroup
    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            dur, err := provider.Ping(host)
            if err != nil {
                dur = -1
            }
            mu.Lock()
            results[host] = dur
            mu.Unlock()
        }(h)
    }
    wg.Wait()
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: nightly-concurrent-ping host1 [host2 ...]")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    provider := RealPingProvider{}
    results := PingHosts(provider, hosts)
    var total time.Duration
    var count int
    for _, h := range hosts {
        dur := results[h]
        if dur < 0 {
            fmt.Printf("%s: unreachable\n", h)
        } else {
            fmt.Printf("%s: %v\n", h, dur)
            total += dur
            count++
        }
    }
    if count > 0 {
        avg := total / time.Duration(count)
        fmt.Printf("Average latency: %v\n", avg)
    }
}
