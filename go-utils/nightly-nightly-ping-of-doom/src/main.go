package main

import (
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

var PingFunc = defaultPing

func defaultPing(host string, timeout time.Duration) (time.Duration, error) {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), timeout)
    if err != nil {
        return 0, err
    }
    conn.Close()
    return time.Since(start), nil
}

type result struct {
    host string
    dur  time.Duration
    err  error
}

func aggregate(hosts []string, timeout time.Duration) (time.Duration, time.Duration, time.Duration, error) {
    if len(hosts) == 0 {
        return 0, 0, 0, fmt.Errorf("no hosts provided")
    }
    results := make(chan result, len(hosts))
    var wg sync.WaitGroup
    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            d, err := PingFunc(host, timeout)
            results <- result{host: host, dur: d, err: err}
        }(h)
    }
    wg.Wait()
    close(results)

    var min, max, sum time.Duration
    count := 0
    for r := range results {
        if r.err != nil {
            // skip failed pings in statistics
            continue
        }
        if count == 0 || r.dur < min {
            min = r.dur
        }
        if r.dur > max {
            max = r.dur
        }
        sum += r.dur
        count++
    }
    if count == 0 {
        return 0, 0, 0, fmt.Errorf("all pings failed")
    }
    avg := time.Duration(int64(sum) / int64(count))
    return min, avg, max, nil
}

func main() {
    timeout := 2 * time.Second
    hosts := os.Args[1:]
    if len(hosts) == 0 {
        fmt.Println("Usage: ping-of-doom <host1> <host2> ...")
        os.Exit(1)
    }
    min, avg, max, err := aggregate(hosts, timeout)
    if err != nil {
        fmt.Fprintf(os.Stderr, "Error: %v\n", err)
        os.Exit(1)
    }
    fmt.Printf("Ping stats (ms) - min: %d, avg: %d, max: %d\n", min.Milliseconds(), avg.Milliseconds(), max.Milliseconds())
}
