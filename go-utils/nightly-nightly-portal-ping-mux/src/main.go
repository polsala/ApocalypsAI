package main

import (
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

type PingResult struct {
    Address string
    Latency time.Duration
    Err     error
}

// pingHost attempts to open a TCP connection to addr using the provided dialer.
// It returns the latency measured and any error encountered.
func pingHost(addr string, dialer func(network, address string) (net.Conn, error)) PingResult {
    start := time.Now()
    conn, err := dialer("tcp", addr)
    latency := time.Since(start)
    if err == nil && conn != nil {
        conn.Close()
    }
    return PingResult{Address: addr, Latency: latency, Err: err}
}

// computeStats returns min, avg, max latency from a slice of durations.
func computeStats(latencies []time.Duration) (min, avg, max time.Duration) {
    if len(latencies) == 0 {
        return 0, 0, 0
    }
    min = latencies[0]
    max = latencies[0]
    var sum time.Duration
    for _, d := range latencies {
        if d < min {
            min = d
        }
        if d > max {
            max = d
        }
        sum += d
    }
    avg = sum / time.Duration(len(latencies))
    return
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: portal-ping <host:port> [<host:port> ...]")
        os.Exit(1)
    }
    addresses := os.Args[1:]
    resultsCh := make(chan PingResult, len(addresses))
    var wg sync.WaitGroup
    for _, addr := range addresses {
        wg.Add(1)
        go func(a string) {
            defer wg.Done()
            res := pingHost(a, net.DialTimeout)
            resultsCh <- res
        }(addr)
    }
    wg.Wait()
    close(resultsCh)

    var latencies []time.Duration
    for res := range resultsCh {
        if res.Err != nil {
            fmt.Printf("Failed to open portal to %s – error: %v\n", res.Address, res.Err)
            continue
        }
        fmt.Printf("Portal opened to %s – latency: %.2fms\n", res.Address, float64(res.Latency.Microseconds())/1000.0)
        latencies = append(latencies, res.Latency)
    }

    if len(latencies) == 0 {
        fmt.Println("No successful pings – cannot compute stats.")
        return
    }
    min, avg, max := computeStats(latencies)
    fmt.Printf("\nLatency stats – min: %.2fms | avg: %.2fms | max: %.2fms\n",
        float64(min.Microseconds())/1000.0,
        float64(avg.Microseconds())/1000.0,
        float64(max.Microseconds())/1000.0)
}
