package main

import (
    "encoding/json"
    "flag"
    "fmt"
    "net/http"
    "os"
    "sync"
    "time"
)

type Result struct {
    URL        string  `json:"url"`
    StatusCode int     `json:"status_code,omitempty"`
    DurationMs float64 `json:"duration_ms,omitempty"`
    Error      string  `json:"error,omitempty"`
}

func ping(url string, timeout time.Duration) Result {
    client := http.Client{Timeout: timeout}
    start := time.Now()
    resp, err := client.Get(url)
    elapsed := time.Since(start).Seconds() * 1000 // milliseconds
    if err != nil {
        return Result{URL: url, Error: err.Error()}
    }
    defer resp.Body.Close()
    return Result{URL: url, StatusCode: resp.StatusCode, DurationMs: elapsed}
}

func main() {
    timeout := flag.Int("timeout", 5, "request timeout in seconds")
    flag.Parse()
    urls := flag.Args()
    if len(urls) == 0 {
        fmt.Fprintln(os.Stderr, "Usage: network-pulse [options] <url1> <url2> ...")
        os.Exit(1)
    }

    var wg sync.WaitGroup
    results := make([]Result, len(urls))
    for i, u := range urls {
        wg.Add(1)
        go func(idx int, url string) {
            defer wg.Done()
            results[idx] = ping(url, time.Duration(*timeout)*time.Second)
        }(i, u)
    }
    wg.Wait()

    out, _ := json.MarshalIndent(results, "", "  ")
    fmt.Println(string(out))
}
