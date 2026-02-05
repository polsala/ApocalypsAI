package main

import (
    "flag"
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

// dialFunc is a variable so tests can replace it with a mock.
var dialFunc = net.DialTimeout

// pingHost attempts to open a TCP connection to the host on port 80 and measures latency.
func pingHost(host string, timeout time.Duration) (time.Duration, error) {
    start := time.Now()
    conn, err := dialFunc("tcp", net.JoinHostPort(host, "80"), timeout)
    if err != nil {
        return 0, err
    }
    _ = conn.Close()
    return time.Since(start), nil
}

// pingAll pings each host concurrently respecting the max concurrency limit.
func pingAll(hosts []string, timeout time.Duration, maxConcurrency int) []Result {
    var wg sync.WaitGroup
    sem := make(chan struct{}, maxConcurrency)
    results := make([]Result, len(hosts))

    for i, h := range hosts {
        wg.Add(1)
        go func(idx int, host string) {
            defer wg.Done()
            sem <- struct{}{}
            latency, err := pingHost(host, timeout)
            results[idx] = Result{Host: host, Latency: latency, Err: err}
            <-sem
        }(i, h)
    }
    wg.Wait()
    return results
}

func formatResult(r Result) string {
    if r.Err != nil {
        return fmt.Sprintf("[%s]\t timeout ❌", r.Host)
    }
    return fmt.Sprintf("[%s]\t %.1fms  ✅", r.Host, float64(r.Latency.Microseconds())/1000.0)
}

func main() {
    hostsFlag := flag.String("hosts", "", "comma‑separated list of hostnames or IPs (required)")
    timeoutFlag := flag.Duration("timeout", 2*time.Second, "per‑host timeout")
    concurrencyFlag := flag.Int("concurrency", 10, "maximum concurrent pings")
    flag.Parse()

    if *hostsFlag == "" {
        fmt.Fprintln(os.Stderr, "error: -hosts flag is required")
        flag.Usage()
        os.Exit(1)
    }

    hosts := strings.Split(*hostsFlag, ",")
    fmt.Println("⚡️ Scanning the wasteland…")
    results := pingAll(hosts, *timeoutFlag, *concurrencyFlag)

    reachable := 0
    for _, r := range results {
        fmt.Println(formatResult(r))
        if r.Err == nil {
            reachable++
        }
    }
    fmt.Printf("\n🛡️ All done. %d/%d hosts reachable.\n", reachable, len(hosts))
}
