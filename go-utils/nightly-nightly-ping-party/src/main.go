package main

import (
    "bufio"
    "encoding/json"
    "flag"
    "fmt"
    "net"
    "os"
    "strings"
    "sync"
    "time"
)

type Result struct {
    Host      string   `json:"host"`
    LatencyMs *float64 `json:"latency_ms,omitempty"`
    Error     *string  `json:"error,omitempty"`
}

// PingHost attempts a TCP connection to the given host on port 80 and measures the round‑trip time.
// It returns the latency in milliseconds or an error if the connection could not be established.
func PingHost(host string, timeout time.Duration) (float64, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), timeout)
    if err != nil {
        return 0, err
    }
    conn.Close()
    elapsed := time.Since(start).Seconds() * 1000 // convert to ms
    return elapsed, nil
}

func main() {
    timeoutFlag := flag.Duration("timeout", 2*time.Second, "connection timeout")
    flag.Parse()
    hosts := []string{}
    // If positional arguments are provided, use them; otherwise read from stdin.
    if flag.NArg() > 0 {
        hosts = flag.Args()
    } else {
        scanner := bufio.NewScanner(os.Stdin)
        for scanner.Scan() {
            line := strings.TrimSpace(scanner.Text())
            if line != "" {
                hosts = append(hosts, line)
            }
        }
    }

    var wg sync.WaitGroup
    results := make([]Result, len(hosts))
    for i, h := range hosts {
        wg.Add(1)
        go func(idx int, host string) {
            defer wg.Done()
            latency, err := PingHost(host, *timeoutFlag)
            if err != nil {
                errStr := err.Error()
                results[idx] = Result{Host: host, Error: &errStr}
            } else {
                lat := latency
                results[idx] = Result{Host: host, LatencyMs: &lat}
            }
        }(i, h)
    }
    wg.Wait()
    output := map[string][]Result{"results": results}
    enc := json.NewEncoder(os.Stdout)
    enc.SetIndent("", "  ")
    if err := enc.Encode(output); err != nil {
        fmt.Fprintln(os.Stderr, "failed to encode output:", err)
        os.Exit(1)
    }
}
