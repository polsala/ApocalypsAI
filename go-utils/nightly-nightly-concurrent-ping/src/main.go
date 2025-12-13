package main

import (
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

// PingFunc is a variable so tests can replace it.
var PingFunc = PingHost

// PingHost measures latency to host by opening a TCP connection to port 80.
func PingHost(host string) (int, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), 2*time.Second)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return int(time.Since(start).Milliseconds()), nil
}

// PingAll pings each host concurrently and returns a map of host->latency.
func PingAll(hosts []string) map[string]int {
    results := make(map[string]int)
    var mu sync.Mutex
    var wg sync.WaitGroup

    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            if latency, err := PingFunc(host); err == nil {
                mu.Lock()
                results[host] = latency
                mu.Unlock()
            } else {
                mu.Lock()
                results[host] = -1 // indicate failure
                mu.Unlock()
            }
        }(h)
    }
    wg.Wait()
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: nightly-concurrent-ping <host1> <host2> ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    results := PingAll(hosts)
    for _, h := range hosts {
        if results[h] >= 0 {
            fmt.Printf("%s: %dms\n", h, results[h])
        } else {
            fmt.Printf("%s: unreachable\n", h)
        }
    }
}
