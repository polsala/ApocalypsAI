package main

import (
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

type LatencyProvider func(host string) (int, error)

func realProvider(host string) (int, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), 2*time.Second)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return int(time.Since(start).Milliseconds()), nil
}

func PingHosts(hosts []string, provider LatencyProvider) map[string]int {
    results := make(map[string]int)
    var mu sync.Mutex
    var wg sync.WaitGroup
    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            latency, err := provider(host)
            if err != nil {
                latency = -1 // indicate failure
            }
            mu.Lock()
            results[host] = latency
            mu.Unlock()
        }(h)
    }
    wg.Wait()
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: go run src/main.go <host1> <host2> ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    results := PingHosts(hosts, realProvider)
    for _, h := range hosts {
        lat := results[h]
        if lat < 0 {
            fmt.Printf("%s: unreachable\n", h)
        } else {
            fmt.Printf("%s: %dms\n", h, lat)
        }
    }
}
