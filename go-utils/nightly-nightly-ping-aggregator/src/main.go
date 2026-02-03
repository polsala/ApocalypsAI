package main

import (
    "context"
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

type Dialer interface {
    DialContext(ctx context.Context, network, address string) (net.Conn, error)
}

// PingHost attempts a TCP connection to the given address using the provided Dialer.
// It returns the elapsed time if successful, or an error otherwise.
func PingHost(d Dialer, address string, timeout time.Duration) (time.Duration, error) {
    ctx, cancel := context.WithTimeout(context.Background(), timeout)
    defer cancel()
    start := time.Now()
    conn, err := d.DialContext(ctx, "tcp", address)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

// PingAll pings each address concurrently and returns a map of address to latency.
// A negative duration indicates the host was unreachable.
func PingAll(d Dialer, addresses []string, timeout time.Duration) map[string]time.Duration {
    results := make(map[string]time.Duration)
    var mu sync.Mutex
    var wg sync.WaitGroup
    for _, addr := range addresses {
        wg.Add(1)
        go func(a string) {
            defer wg.Done()
            dur, err := PingHost(d, a, timeout)
            if err != nil {
                dur = -1
            }
            mu.Lock()
            results[a] = dur
            mu.Unlock()
        }(addr)
    }
    wg.Wait()
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: ping-aggregator <host:port> [<host:port> ...]")
        os.Exit(1)
    }
    addresses := os.Args[1:]
    timeout := 2 * time.Second
    d := &net.Dialer{}
    results := PingAll(d, addresses, timeout)
    for addr, dur := range results {
        if dur < 0 {
            fmt.Printf("%s: unreachable\n", addr)
        } else {
            fmt.Printf("%s: %v\n", addr, dur)
        }
    }
}
