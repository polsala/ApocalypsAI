package main

import (
    "context"
    "encoding/json"
    "flag"
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

// Dialer abstracts net.Dialer for easier testing.
type Dialer interface {
    DialContext(ctx context.Context, network, address string) (net.Conn, error)
}

// PingHost attempts a TCP connection to the given host and returns the elapsed time.
func PingHost(d Dialer, host string, timeout time.Duration) (time.Duration, error) {
    ctx, cancel := context.WithTimeout(context.Background(), timeout)
    defer cancel()
    start := time.Now()
    conn, err := d.DialContext(ctx, "tcp", host)
    if err != nil {
        return 0, err
    }
    _ = conn.Close()
    return time.Since(start), nil
}

// PingHosts concurrently pings a slice of hosts and returns a map of hostâlatency (ms).
func PingHosts(d Dialer, hosts []string, timeout time.Duration) map[string]float64 {
    results := make(map[string]float64)
    var mu sync.Mutex
    var wg sync.WaitGroup
    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            dur, err := PingHost(d, host, timeout)
            var ms float64
            if err == nil {
                ms = float64(dur.Milliseconds())
            } else {
                ms = 0
            }
            mu.Lock()
            results[host] = ms
            mu.Unlock()
        }(h)
    }
    wg.Wait()
    return results
}

func main() {
    timeoutSec := flag.Int("t", 3, "timeout in seconds for each host")
    flag.Parse()
    hosts := flag.Args()
    if len(hosts) == 0 {
        fmt.Fprintln(os.Stderr, "Usage: ping-sweeper -t <seconds> host1:port host2:port ...")
        os.Exit(1)
    }
    timeout := time.Duration(*timeoutSec) * time.Second
    dialer := &net.Dialer{}
    results := PingHosts(dialer, hosts, timeout)
    enc := json.NewEncoder(os.Stdout)
    enc.SetEscapeHTML(false)
    if err := enc.Encode(results); err != nil {
        fmt.Fprintln(os.Stderr, "Failed to encode JSON:", err)
        os.Exit(1)
    }
}

