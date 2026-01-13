package main

import (
    "fmt"
    "net"
    "os"
    "strings"
    "sync"
    "time"
)

type Result struct {
    Host    string
    Latency time.Duration
    Err     error
}

func pingHost(host string, timeout time.Duration) Result {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", host, timeout)
    latency := time.Since(start)
    if err == nil {
        conn.Close()
    }
    return Result{Host: host, Latency: latency, Err: err}
}

func pingHosts(hosts []string, timeout time.Duration) []Result {
    var wg sync.WaitGroup
    results := make([]Result, len(hosts))
    for i, h := range hosts {
        wg.Add(1)
        go func(idx int, host string) {
            defer wg.Done()
            results[idx] = pingHost(host, timeout)
        }(i, h)
    }
    wg.Wait()
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: portal-ping <host1:port,host2:port,...>")
        os.Exit(1)
    }
    input := os.Args[1]
    hosts := strings.Split(input, ",")
    timeout := 2 * time.Second
    results := pingHosts(hosts, timeout)
    fmt.Printf("%-25s %-10s %s
", "HOST", "LATENCY", "STATUS")
    for _, r := range results {
        status := "OK"
        if r.Err != nil {
            status = r.Err.Error()
        }
        fmt.Printf("%-25s %-10s %s
", r.Host, r.Latency, status)
    }
}

