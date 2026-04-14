package main

import (
    "fmt"
    "io"
    "net/http"
    "os"
    "sync"
    "time"
)

type result struct {
    url      string
    duration time.Duration
    err      error
}

func ping(url string, wg *sync.WaitGroup, ch chan<- result) {
    defer wg.Done()
    start := time.Now()
    client := http.Client{Timeout: 5 * time.Second}
    resp, err := client.Get(url)
    if err == nil {
        // Drain body to completion
        _, _ = io.Copy(io.Discard, resp.Body)
        resp.Body.Close()
    }
    elapsed := time.Since(start)
    ch <- result{url: url, duration: elapsed, err: err}
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: echo-chronicle <url1> <url2> ...")
        os.Exit(1)
    }
    urls := os.Args[1:]

    var wg sync.WaitGroup
    ch := make(chan result, len(urls))

    for _, u := range urls {
        wg.Add(1)
        go ping(u, &wg, ch)
    }
    wg.Wait()
    close(ch)

    var results []result
    for r := range ch {
        results = append(results, r)
    }

    fmt.Println("🔔 Echo Chronicle Report")
    var sum time.Duration
    var min, max time.Duration
    for i, r := range results {
        if r.err != nil {
            fmt.Printf("❌ %s – error: %s\n", r.url, r.err)
            continue
        }
        fmt.Printf("✅ %s – %dms\n", r.url, r.duration.Milliseconds())
        sum += r.duration
        if i == 0 || r.duration < min {
            min = r.duration
        }
        if r.duration > max {
            max = r.duration
        }
    }
    if len(results) > 0 {
        avg := sum / time.Duration(len(results))
        fmt.Printf("📊 Summary: min=%dms, avg=%dms, max=%dms\n", min.Milliseconds(), avg.Milliseconds(), max.Milliseconds())
    }
}
