package main

import (
    "bufio"
    "context"
    "flag"
    "fmt"
    "net/http"
    "os"
    "strings"
    "sync"
    "sync/atomic"
    "time"
)

type Stats struct {
    Total        int64
    Success      int64
    Failure      int64
    TotalLatency int64 // nanoseconds
}

// run performs the traffic simulation and returns aggregated statistics.
func run(urls []string, concurrency int, duration time.Duration) Stats {
    var stats Stats
    if len(urls) == 0 || concurrency <= 0 {
        return stats
    }

    ctx, cancel := context.WithTimeout(context.Background(), duration)
    defer cancel()

    // channel to feed URLs to workers (cycling through the list)
    urlCh := make(chan string)
    wg := sync.WaitGroup{}

    // start workers
    for i := 0; i < concurrency; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            client := http.Client{Timeout: 5 * time.Second}
            for {
                select {
                case <-ctx.Done():
                    return
                case u := <-urlCh:
                    start := time.Now()
                    resp, err := client.Get(u)
                    latency := time.Since(start).Nanoseconds()
                    atomic.AddInt64(&stats.Total, 1)
                    atomic.AddInt64(&stats.TotalLatency, latency)
                    if err != nil {
                        atomic.AddInt64(&stats.Failure, 1)
                        continue
                    }
                    resp.Body.Close()
                    if resp.StatusCode >= 200 && resp.StatusCode < 300 {
                        atomic.AddInt64(&stats.Success, 1)
                    } else {
                        atomic.AddInt64(&stats.Failure, 1)
                    }
                }
            }
        }()
    }

    // feed URLs until the context expires
    go func() {
        defer close(urlCh)
        idx := 0
        for {
            select {
            case <-ctx.Done():
                return
            case urlCh <- urls[idx%len(urls)]:
                idx++
            }
        }
    }()

    wg.Wait()
    return stats
}

func loadURLsFromFile(path string) ([]string, error) {
    file, err := os.Open(path)
    if err != nil {
        return nil, err
    }
    defer file.Close()
    var urls []string
    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line != "" {
            urls = append(urls, line)
        }
    }
    return urls, scanner.Err()
}

func main() {
    var (
        urlsFlag        string
        fileFlag        string
        concurrencyFlag int
        durationFlag    string
    )
    flag.StringVar(&urlsFlag, "urls", "", "comma‑separated list of target URLs")
    flag.StringVar(&fileFlag, "file", "", "path to file containing URLs (one per line)")
    flag.IntVar(&concurrencyFlag, "concurrency", 5, "number of parallel workers")
    flag.StringVar(&durationFlag, "duration", "10s", "simulation duration (e.g., 10s, 2m)")
    flag.Parse()

    var urls []string
    if urlsFlag != "" {
        for _, u := range strings.Split(urlsFlag, ",") {
            u = strings.TrimSpace(u)
            if u != "" {
                urls = append(urls, u)
            }
        }
    }
    if fileFlag != "" {
        fileURLs, err := loadURLsFromFile(fileFlag)
        if err != nil {
            fmt.Fprintf(os.Stderr, "error reading URL file: %v\n", err)
            os.Exit(1)
        }
        urls = append(urls, fileURLs...)
    }
    if len(urls) == 0 {
        fmt.Fprintln(os.Stderr, "no URLs provided; use -urls or -file flag")
        os.Exit(1)
    }

    dur, err := time.ParseDuration(durationFlag)
    if err != nil {
        fmt.Fprintf(os.Stderr, "invalid duration: %v\n", err)
        os.Exit(1)
    }

    stats := run(urls, concurrencyFlag, dur)
    avgLatency := time.Duration(0)
    if stats.Total > 0 {
        avgLatency = time.Duration(stats.TotalLatency / stats.Total)
    }
    fmt.Printf("Total requests: %d\n", stats.Total)
    fmt.Printf("Successful: %d\n", stats.Success)
    fmt.Printf("Failed: %d\n", stats.Failure)
    fmt.Printf("Average latency: %s\n", avgLatency)
}
