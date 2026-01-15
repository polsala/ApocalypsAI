package main

import (
    "fmt"
    "net"
    "os"
    "time"
)

// PingHost attempts a TCP connection to the given host:port and returns the elapsed time.
// If the connection cannot be established within the timeout, an error is returned.
func PingHost(host string, timeout time.Duration) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", host, timeout)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

// PingMultiple pings all hosts concurrently and returns a map of host to latency.
// Unreachable hosts are recorded with a negative duration.
func PingMultiple(hosts []string, timeout time.Duration) map[string]time.Duration {
    results := make(map[string]time.Duration)
    ch := make(chan struct{})
    for _, h := range hosts {
        go func(host string) {
            dur, err := PingHost(host, timeout)
            if err != nil {
                dur = -1
            }
            results[host] = dur
            ch <- struct{}{}
        }(h)
    }
    for range hosts {
        <-ch
    }
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: portal-ping <host1:port> [host2:port] ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    timeout := 2 * time.Second
    results := PingMultiple(hosts, timeout)
    for _, h := range hosts {
        dur := results[h]
        if dur < 0 {
            fmt.Printf("%s: unreachable\n", h)
        } else {
            fmt.Printf("%s: %d ms\n", h, dur.Milliseconds())
        }
    }
}
