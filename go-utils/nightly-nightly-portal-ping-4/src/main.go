package main

import (
    "fmt"
    "net/http"
    "os"
    "sync"
    "time"
)

type Result struct {
    URL     string
    Latency time.Duration
    Err     error
}

func ping(url string) Result {
    start := time.Now()
    client := http.Client{Timeout: 5 * time.Second}
    req, err := http.NewRequest("HEAD", url, nil)
    if err != nil {
        return Result{URL: url, Err: err}
    }
    resp, err := client.Do(req)
    if err != nil {
        return Result{URL: url, Err: err}
    }
    resp.Body.Close()
    return Result{URL: url, Latency: time.Since(start)}
}

func statusMessage(latency time.Duration) string {
    ms := latency.Milliseconds()
    switch {
    case ms < 100:
        return "Radiant"
    case ms < 300:
        return "Flickering"
    default:
        return "Dim"
    }
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: portal-ping <url1> [url2 ...]")
        os.Exit(1)
    }
    urls := os.Args[1:]

    var wg sync.WaitGroup
    resultsCh := make(chan Result, len(urls))

    for _, u := range urls {
        wg.Add(1)
        go func(u string) {
            defer wg.Done()
            resultsCh <- ping(u)
        }(u)
    }

    wg.Wait()
    close(resultsCh)

    for r := range resultsCh {
        if r.Err != nil {
            fmt.Printf("%s – ❌ Error: %v\n", r.URL, r.Err)
            continue
        }
        fmt.Printf("%s – %d ms – %s\n", r.URL, r.Latency.Milliseconds(), statusMessage(r.Latency))
    }
}
