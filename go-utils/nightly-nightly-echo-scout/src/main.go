package main

import (
    "fmt"
    "io"
    "net/http"
    "os"
    "sync"
    "time"
)

type Result struct {
    URL      string
    Duration time.Duration
    Err      error
}

func PingURL(url string) Result {
    start := time.Now()
    resp, err := http.Get(url)
    if err != nil {
        return Result{URL: url, Duration: 0, Err: err}
    }
    // Drain body to completion
    _, _ = io.Copy(io.Discard, resp.Body)
    resp.Body.Close()
    return Result{URL: url, Duration: time.Since(start), Err: nil}
}

func PingURLs(urls []string) []Result {
    var wg sync.WaitGroup
    results := make([]Result, len(urls))
    for i, u := range urls {
        wg.Add(1)
        go func(idx int, url string) {
            defer wg.Done()
            results[idx] = PingURL(url)
        }(i, u)
    }
    wg.Wait()
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: nightly-echo-scout <url1> <url2> ...")
        os.Exit(1)
    }
    urls := os.Args[1:]
    results := PingURLs(urls)
    for _, r := range results {
        if r.Err != nil {
            fmt.Printf("❌ %s - Error: %v\n", r.URL, r.Err)
        } else {
            fmt.Printf("🔊 %s - Signal received in %dms 🎶\n", r.URL, r.Duration.Milliseconds())
        }
    }
}
