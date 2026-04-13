package main

import (
    "bufio"
    "errors"
    "flag"
    "fmt"
    "net"
    "os"
    "strings"
    "sync"
    "time"
)

type PingResult struct {
    Host    string
    Latency time.Duration
    Err     error
}

// ping attempts a TCP connection to the host on port 80 and measures latency.
func ping(host string, timeout time.Duration) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), timeout)
    if err != nil {
        return 0, err
    }
    _ = conn.Close()
    return time.Since(start), nil
}

// emojiForResult returns a whimsical emoji based on latency or error.
func emojiForResult(latency time.Duration, err error) string {
    if err != nil {
        return "⚰️"
    }
    switch {
    case latency < 100*time.Millisecond:
        return "👻"
    case latency < 300*time.Millisecond:
        return "🕸️"
    default:
        return "🧟"
    }
}

func loadHostsFromFile(path string) ([]string, error) {
    file, err := os.Open(path)
    if err != nil {
        return nil, err
    }
    defer file.Close()
    var hosts []string
    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line != "" {
            hosts = append(hosts, line)
        }
    }
    if err := scanner.Err(); err != nil {
        return nil, err
    }
    return hosts, nil
}

func main() {
    filePtr := flag.String("f", "", "Path to file containing hosts (one per line)")
    timeoutPtr := flag.Duration("t", 2*time.Second, "Connection timeout per host")
    flag.Parse()

    var hosts []string
    if *filePtr != "" {
        var err error
        hosts, err = loadHostsFromFile(*filePtr)
        if err != nil {
            fmt.Fprintf(os.Stderr, "Error reading hosts file: %v\n", err)
            os.Exit(1)
        }
    }
    hosts = append(hosts, flag.Args()...)
    if len(hosts) == 0 {
        fmt.Fprintln(os.Stderr, "No hosts provided. Use arguments or -f flag.")
        os.Exit(1)
    }

    resultsCh := make(chan PingResult, len(hosts))
    var wg sync.WaitGroup
    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            lat, err := ping(host, *timeoutPtr)
            resultsCh <- PingResult{Host: host, Latency: lat, Err: err}
        }(h)
    }
    wg.Wait()
    close(resultsCh)

    fmt.Printf("%-20s %-10s %s\n", "Host", "Latency", "Status")
    for res := range resultsCh {
        latencyStr := "—"
        if res.Err == nil {
            latencyStr = fmt.Sprintf("%dms", res.Latency.Milliseconds())
        }
        fmt.Printf("%-20s %-10s %s\n", res.Host, latencyStr, emojiForResult(res.Latency, res.Err))
    }
}
