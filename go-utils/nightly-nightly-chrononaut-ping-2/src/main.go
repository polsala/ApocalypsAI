package main

import (
    "context"
    "encoding/json"
    "flag"
    "fmt"
    "net"
    "os"
    "strings"
    "sync"
    "time"
)

type PingResult struct {
    Host          string  `json:"host"`
    AvgLatencyMs  float64 `json:"avg_latency_ms"`
    Success       bool    `json:"success"`
}

type Output struct {
    Results []PingResult `json:"results"`
}

// PingFunc abstracts the ping operation for easier testing.
// It returns the latency for a single attempt or an error.
var PingFunc = RealPing

// RealPing performs a TCP connection to the host on port 80 and measures latency.
func RealPing(ctx context.Context, host string, timeout time.Duration) (time.Duration, error) {
    d := net.Dialer{Timeout: timeout}
    start := time.Now()
    conn, err := d.DialContext(ctx, "tcp", net.JoinHostPort(host, "80"))
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

func pingHost(ctx context.Context, host string, count int, timeout time.Duration) PingResult {
    var total time.Duration
    successCount := 0
    for i := 0; i < count; i++ {
        lat, err := PingFunc(ctx, host, timeout)
        if err == nil {
            total += lat
            successCount++
        }
    }
    if successCount == 0 {
        return PingResult{Host: host, AvgLatencyMs: 0, Success: false}
    }
    avgMs := float64(total.Milliseconds()) / float64(successCount)
    return PingResult{Host: host, AvgLatencyMs: avgMs, Success: true}
}

func main() {
    hostsFlag := flag.String("hosts", "", "Comma‑separated list of hostnames or IPs")
    countFlag := flag.Int("count", 1, "Number of ping attempts per host")
    timeoutFlag := flag.Int("timeout", 2, "Per‑attempt timeout in seconds")
    flag.Parse()

    if *hostsFlag == "" {
        fmt.Fprintln(os.Stderr, "Error: -hosts flag is required")
        os.Exit(1)
    }
    hosts := strings.Split(*hostsFlag, ",")
    timeout := time.Duration(*timeoutFlag) * time.Second

    ctx := context.Background()
    var wg sync.WaitGroup
    results := make([]PingResult, len(hosts))

    for i, h := range hosts {
        wg.Add(1)
        go func(idx int, host string) {
            defer wg.Done()
            results[idx] = pingHost(ctx, strings.TrimSpace(host), *countFlag, timeout)
        }(i, h)
    }
    wg.Wait()

    out := Output{Results: results}
    enc := json.NewEncoder(os.Stdout)
    enc.SetIndent("", "  ")
    if err := enc.Encode(out); err != nil {
        fmt.Fprintln(os.Stderr, "Failed to encode JSON:", err)
        os.Exit(1)
    }
}
