package main

import (
    "bufio"
    "encoding/json"
    "fmt"
    "net"
    "os"
    "strings"
    "sync"
    "time"
)

type Result struct {
    Host      string `json:"host"`
    Reachable bool   `json:"reachable"`
    LatencyMs int64  `json:"latency_ms"`
}

// dialer is a variable so tests can replace it with a mock implementation.
var dialer = func(network, address string, timeout time.Duration) (net.Conn, error) {
    return net.DialTimeout(network, address, timeout)
}

func pingHost(host string, timeout time.Duration) Result {
    start := time.Now()
    conn, err := dialer("tcp", host, timeout)
    if err != nil {
        return Result{Host: host, Reachable: false, LatencyMs: 0}
    }
    conn.Close()
    latency := time.Since(start).Milliseconds()
    return Result{Host: host, Reachable: true, LatencyMs: latency}
}

func PingHosts(hosts []string, timeout time.Duration, workers int) []Result {
    var wg sync.WaitGroup
    in := make(chan string)
    out := make(chan Result)

    // Start worker goroutines.
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for h := range in {
                out <- pingHost(h, timeout)
            }
        }()
    }

    // Close out channel when all workers are done.
    go func() {
        wg.Wait()
        close(out)
    }()

    // Feed hosts into the input channel.
    go func() {
        for _, h := range hosts {
            in <- h
        }
        close(in)
    }()

    var results []Result
    for r := range out {
        results = append(results, r)
    }
    return results
}

func readHostsFromStdin() []string {
    var hosts []string
    scanner := bufio.NewScanner(os.Stdin)
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line != "" {
            hosts = append(hosts, line)
        }
    }
    return hosts
}

func main() {
    var hosts []string
    if len(os.Args) > 1 {
        hosts = os.Args[1:]
    } else {
        hosts = readHostsFromStdin()
    }
    if len(hosts) == 0 {
        fmt.Fprintln(os.Stderr, "No hosts provided")
        os.Exit(1)
    }
    results := PingHosts(hosts, 2*time.Second, 10)
    enc := json.NewEncoder(os.Stdout)
    enc.SetIndent("", "  ")
    enc.Encode(results)
}
