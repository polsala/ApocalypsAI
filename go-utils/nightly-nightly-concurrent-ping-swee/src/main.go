package main

import (
    "bufio"
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

type pingResult struct {
    host    string
    latency time.Duration
    err     error
}

// pingFunc is a variable so tests can replace it.
var pingFunc = defaultPing

func defaultPing(host string) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), 2*time.Second)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

func pingHost(host string, wg *sync.WaitGroup, ch chan<- pingResult) {
    defer wg.Done()
    lat, err := pingFunc(host)
    ch <- pingResult{host: host, latency: lat, err: err}
}

func main() {
    hosts := os.Args[1:]
    if len(hosts) == 0 {
        scanner := bufio.NewScanner(os.Stdin)
        for scanner.Scan() {
            line := scanner.Text()
            if line != "" {
                hosts = append(hosts, line)
            }
        }
    }
    if len(hosts) == 0 {
        fmt.Fprintln(os.Stderr, "No hosts provided")
        os.Exit(1)
    }

    var wg sync.WaitGroup
    resultsCh := make(chan pingResult, len(hosts))

    for _, h := range hosts {
        wg.Add(1)
        go pingHost(h, &wg, resultsCh)
    }
    wg.Wait()
    close(resultsCh)

    var total time.Duration
    var count int
    for r := range resultsCh {
        if r.err != nil {
            fmt.Fprintf(os.Stderr, "error pinging %s: %v\n", r.host, r.err)
            continue
        }
        total += r.latency
        count++
    }
    if count == 0 {
        fmt.Fprintln(os.Stderr, "All pings failed")
        os.Exit(1)
    }
    avg := total / time.Duration(count)
    fmt.Printf("Average latency: %s\n", avg)
}
