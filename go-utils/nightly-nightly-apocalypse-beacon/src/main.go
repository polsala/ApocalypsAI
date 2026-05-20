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

type realPingProvider struct {
    timeout time.Duration
}

func (p *realPingProvider) Ping(host string) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", host, p.timeout)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

func pingAll(hosts []string, provider PingProvider) map[string]string {
    var wg sync.WaitGroup
    mu := sync.Mutex{}
    results := make(map[string]string)

    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            dur, err := provider.Ping(host)
            var msg string
            if err != nil {
                msg = fmt.Sprintf("☠️ %s is unreachable (%v)", host, err)
            } else {
                msg = fmt.Sprintf("✅ %s responded in %dms", host, dur.Milliseconds())
            }
            mu.Lock()
            results[host] = msg
            mu.Unlock()
        }(h)
    }
    wg.Wait()
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: beacon <host1:port> [host2:port] ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    provider := &realPingProvider{timeout: 2 * time.Second}
    results := pingAll(hosts, provider)
    for _, h := range hosts {
        fmt.Println(results[h])
    }
}
