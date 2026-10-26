package main

import (
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

type DialerFunc func(host string, timeout time.Duration) (time.Duration, error)

func realDialer(host string, timeout time.Duration) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), timeout)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

// PingHosts pings each host concurrently using the provided dialer.
// If the dialer returns an error, the latency is recorded as -1.
func PingHosts(hosts []string, timeout time.Duration, dialer DialerFunc) map[string]time.Duration {
    results := make(map[string]time.Duration)
    var wg sync.WaitGroup
    var mu sync.Mutex
    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            dur, err := dialer(host, timeout)
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
        fmt.Println("Usage: portal-ping <host1> [host2] ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    timeout := 2 * time.Second
    results := PingHosts(hosts, timeout, realDialer)

    var total time.Duration
    var count int
    var min, max time.Duration
    for host, d := range results {
        if d < 0 {
            fmt.Printf("%s: unreachable\n", host)
            continue
        }
        fmt.Printf("%s: %v\n", host, d)
        if count == 0 || d < min {
            min = d
        }
        if d > max {
            max = d
        }
        total += d
        count++
    }
    if count > 0 {
        avg := total / time.Duration(count)
        fmt.Printf("\nSummary: min=%v avg=%v max=%v (over %d hosts)\n", min, avg, max, count)
    }
}
