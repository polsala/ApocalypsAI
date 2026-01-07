package main

import (
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
    Host    string  `json:"host"`
    Success bool    `json:"success"`
    Latency float64 `json:"latency_ms,omitempty"`
    Error   string  `json:"error,omitempty"`
}

// pingHost attempts a TCP connection to the given host within the timeout.
// It returns a Result containing success status, measured latency, and any error.
func pingHost(host string, timeout time.Duration) Result {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", host, timeout)
    latency := time.Since(start).Seconds() * 1000 // milliseconds
    if err != nil {
        return Result{Host: host, Success: false, Error: err.Error()}
    }
    conn.Close()
    return Result{Host: host, Success: true, Latency: latency}
}

func main() {
    timeoutFlag := flag.Int("t", 1000, "timeout per host in milliseconds")
    flag.Parse()
    hosts := flag.Args()

    // If no hosts on CLI, read from STDIN (one per line)
    if len(hosts) == 0 {
        data, _ := os.ReadFile("/dev/stdin")
        lines := strings.Split(strings.TrimSpace(string(data)), "\n")
        for _, l := range lines {
            if l != "" {
                hosts = append(hosts, strings.TrimSpace(l))
            }
        }
    }

    if len(hosts) == 0 {
        fmt.Fprintln(os.Stderr, "No hosts provided. Pass as arguments or via STDIN.")
        os.Exit(1)
    }

    timeout := time.Duration(*timeoutFlag) * time.Millisecond
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

    enc := json.NewEncoder(os.Stdout)
    enc.SetIndent("", "  ")
    if err := enc.Encode(results); err != nil {
        fmt.Fprintln(os.Stderr, "Failed to encode JSON:", err)
        os.Exit(1)
    }
}
