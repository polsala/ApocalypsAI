package main

import (
    "flag"
    "fmt"
    "net/http"
    "sync"
    "time"
)

// pingURL sends a GET request to the given URL with the supplied timeout.
// It returns the elapsed time or an error if the request fails.
func pingURL(url string, timeout time.Duration) (time.Duration, error) {
    client := http.Client{Timeout: timeout}
    start := time.Now()
    resp, err := client.Get(url)
    if err != nil {
        return 0, err
    }
    defer resp.Body.Close()
    return time.Since(start), nil
}

// pingURLs concurrently pings each URL in the slice and returns a map of
// URL -> latency. A negative duration indicates a timeout or error.
func pingURLs(urls []string, timeout time.Duration) map[string]time.Duration {
    results := make(map[string]time.Duration)
    var mu sync.Mutex
    var wg sync.WaitGroup
    for _, u := range urls {
        wg.Add(1)
        go func(u string) {
            defer wg.Done()
            d, err := pingURL(u, timeout)
            if err != nil {
                d = -1
            }
            mu.Lock()
            results[u] = d
            mu.Unlock()
        }(u)
    }
    wg.Wait()
    return results
}

func main() {
    timeout := flag.Int("timeout", 2, "timeout in seconds for each request")
    flag.Parse()
    urls := flag.Args()
    if len(urls) == 0 {
        fmt.Println("Usage: portal-ping-multiplexer [options] <url1> <url2> ...")
        return
    }
    results := pingURLs(urls, time.Duration(*timeout)*time.Second)
    fmt.Println("🌀 Portal Ping Results 🌀")
    for u, d := range results {
        if d < 0 {
            fmt.Printf("%s -> ✖ timeout/error\n", u)
        } else {
            fmt.Printf("%s -> %d ms\n", u, d.Milliseconds())
        }
    }
}
