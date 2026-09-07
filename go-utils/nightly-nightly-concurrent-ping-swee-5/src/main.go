package main

import (
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

type PingResult struct {
    Host    string
    Latency time.Duration
    Err     error
}

// PingFunc is a variable so tests can replace it with a mock implementation.
var PingFunc = realPing

func realPing(host string) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), 2*time.Second)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

func runPings(hosts []string) []PingResult {
    var wg sync.WaitGroup
    resultsCh := make(chan PingResult, len(hosts))
    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            dur, err := PingFunc(host)
            resultsCh <- PingResult{Host: host, Latency: dur, Err: err}
        }(h)
    }
    wg.Wait()
    close(resultsCh)
    var results []PingResult
    for r := range resultsCh {
        results = append(results, r)
    }
    return results
}

func printSummary(results []PingResult) {
    var successCount int
    var totalLatency time.Duration
    for _, r := range results {
        if r.Err != nil {
            fmt.Printf("%s: error (%s)\n", r.Host, r.Err)
        } else {
            fmt.Printf("%s: %s\n", r.Host, r.Latency)
            successCount++
            totalLatency += r.Latency
        }
    }
    failedCount := len(results) - successCount
    avg := time.Duration(0)
    if successCount > 0 {
        avg = totalLatency / time.Duration(successCount)
    }
    fmt.Println("--- Summary ---")
    fmt.Printf("Successful: %d, Failed: %d, Average latency: %s\n", successCount, failedCount, avg)
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: go run ./src/main.go host1 [host2 ...]")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    results := runPings(hosts)
    printSummary(results)
}
