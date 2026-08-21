package main

import (
    "fmt"
    "net"
    "os"
    "sort"
    "sync"
    "time"
)

type PingResult struct {
    Host    string
    Latency time.Duration
    Err     error
}

// pingHost attempts a TCP connection to host:80 and returns latency.
func pingHost(host string) PingResult {
    address := net.JoinHostPort(host, "80")
    start := time.Now()
    conn, err := net.DialTimeout("tcp", address, 2*time.Second)
    latency := time.Since(start)
    if err == nil {
        conn.Close()
    }
    return PingResult{Host: host, Latency: latency, Err: err}
}

// PingHosts pings all hosts concurrently and returns sorted results.
func PingHosts(hosts []string) []PingResult {
    var wg sync.WaitGroup
    resultsCh := make(chan PingResult, len(hosts))

    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            resultsCh <- pingHost(host)
        }(h)
    }

    wg.Wait()
    close(resultsCh)

    var results []PingResult
    for r := range resultsCh {
        results = append(results, r)
    }

    sort.Slice(results, func(i, j int) bool {
        // Successful pings (no error) come first, sorted by latency.
        if results[i].Err == nil && results[j].Err != nil {
            return true
        }
        if results[i].Err != nil && results[j].Err == nil {
            return false
        }
        return results[i].Latency < results[j].Latency
    })
    return results
}

func main() {
    hosts := os.Args[1:]
    if len(hosts) == 0 {
        hosts = []string{"example.com", "google.com", "github.com"}
    }

    results := PingHosts(hosts)

    fmt.Println("⚔️  The wasteland whispers:")
    for _, r := range results {
        if r.Err != nil {
            fmt.Printf("- %s: ❌ unreachable (%v)\n", r.Host, r.Err)
        } else {
            fmt.Printf("- %s: 🌪️ responded in %d ms\n", r.Host, r.Latency.Milliseconds())
        }
    }
}
