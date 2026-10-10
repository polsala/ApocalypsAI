package main

import (
    "fmt"
    "net"
    "time"
)

// PingHost attempts a TCP connection to the given host (host:port) with a timeout.
// It returns the elapsed time if successful, or an error if the connection fails.
func PingHost(host string, timeout time.Duration) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", host, timeout)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

// PingMultiple pings each host in the slice concurrently using the provided timeout.
// It returns a map where the key is the host string and the value is the latency.
// A latency of -1 indicates the host was unreachable.
func PingMultiple(hosts []string, timeout time.Duration) map[string]time.Duration {
    results := make(map[string]time.Duration)
    ch := make(chan struct {
        host string
        dur  time.Duration
        err  error
    })
    for _, h := range hosts {
        go func(host string) {
            dur, err := PingHost(host, timeout)
            if err != nil {
                dur = -1
            }
            ch <- struct {
                host string
                dur  time.Duration
                err  error
            }{host, dur, err}
        }(h)
    }
    for i := 0; i < len(hosts); i++ {
        res := <-ch
        results[res.host] = res.dur
    }
    return results
}

func main() {
    // Example usage: ping a couple of hosts with a 2‑second timeout.
    hosts := []string{"localhost:80", "example.com:80"}
    timeout := 2 * time.Second
    results := PingMultiple(hosts, timeout)
    for h, d := range results {
        if d < 0 {
            fmt.Printf("%s: unreachable\n", h)
        } else {
            fmt.Printf("%s: %v\n", h, d)
        }
    }
}
