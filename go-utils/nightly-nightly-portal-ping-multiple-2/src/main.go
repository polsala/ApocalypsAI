package main

import (
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

type dialerFunc func(network, address string, timeout time.Duration) (net.Conn, error)

// dialer is a variable so tests can replace it with a mock.
var dialer dialerFunc = net.DialTimeout

type result struct {
    host    string
    success bool
    latency time.Duration
    err     error
}

func pingHost(host string, timeout time.Duration) result {
    start := time.Now()
    conn, err := dialer("tcp", net.JoinHostPort(host, "80"), timeout)
    latency := time.Since(start)
    if err != nil {
        return result{host: host, success: false, latency: latency, err: err}
    }
    conn.Close()
    return result{host: host, success: true, latency: latency, err: nil}
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: portal-ping-multiplexer <host1> [host2 ...]")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    timeout := 3 * time.Second
    var wg sync.WaitGroup
    resultsCh := make(chan result, len(hosts))

    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            resultsCh <- pingHost(host, timeout)
        }(h)
    }
    wg.Wait()
    close(resultsCh)

    for r := range resultsCh {
        if r.success {
            fmt.Printf("%s: ✅ %v\n", r.host, r.latency)
        } else {
            fmt.Printf("%s: ❌ %v (%s)\n", r.host, r.latency, r.err)
        }
    }
}
