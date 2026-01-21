package main

import (
    "context"
    "flag"
    "fmt"
    "net/http"
    "strings"
    "sync"
    "time"
)

type result struct {
    url     string
    latency time.Duration
    err     error
}

func pingURL(url string, timeout time.Duration) (time.Duration, error) {
    ctx, cancel := context.WithTimeout(context.Background(), timeout)
    defer cancel()
    start := time.Now()
    req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
    if err != nil {
        return 0, err
    }
    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return 0, err
    }
    defer resp.Body.Close()
    return time.Since(start), nil
}

func categorize(latency time.Duration, err error) string {
    if err != nil {
        return "Lost"
    }
    switch {
    case latency < 100*time.Millisecond:
        return "Radiant"
    case latency < 300*time.Millisecond:
        return "Stable"
    default:
        return "Fading"
    }
}

func main() {
    urlsFlag := flag.String("urls", "", "comma‑separated list of URLs to ping")
    timeoutFlag := flag.Duration("timeout", 5*time.Second, "per‑request timeout")
    flag.Parse()

    if *urlsFlag == "" {
        fmt.Println("No URLs provided. Use -urls flag.")
        return
    }

    urls := strings.Split(*urlsFlag, ",")
    resultsCh := make(chan result, len(urls))
    var wg sync.WaitGroup

    for _, u := range urls {
        wg.Add(1)
        go func(u string) {
            defer wg.Done()
            lat, err := pingURL(strings.TrimSpace(u), *timeoutFlag)
            resultsCh <- result{url: u, latency: lat, err: err}
        }(u)
    }

    wg.Wait()
    close(resultsCh)

    fmt.Printf("%-30s %-10s %-8s\n", "URL", "Latency", "Status")
    fmt.Println(strings.Repeat("-", 55))
    for r := range resultsCh {
        status := categorize(r.latency, r.err)
        latStr := "—"
        if r.err == nil {
            latStr = r.latency.Truncate(time.Millisecond).String()
        }
        fmt.Printf("%-30s %-10s %-8s\n", r.url, latStr, status)
    }
}
