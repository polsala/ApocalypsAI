package main

import (
    "context"
    "fmt"
    "net/http"
    "os"
    "sort"
    "strings"
    "time"
)

type pingResult struct {
    URL      string
    Duration time.Duration
    Err      error
}

// pingHost performs an HTTP GET request to the given URL and returns the round‑trip time.
func pingHost(ctx context.Context, url string) (time.Duration, error) {
    start := time.Now()
    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return 0, err
    }
    // Use a short timeout to avoid hanging forever.
    client := &http.Client{Timeout: 5 * time.Second}
    resp, err := client.Do(req)
    if err != nil {
        return 0, err
    }
    // Drain body to completion.
    _, _ = http.ReadResponse(resp.Body, req)
    resp.Body.Close()
    return time.Since(start), nil
}

func emojiForDuration(d time.Duration) string {
    ms := d.Milliseconds()
    switch {
    case ms < 50:
        return "🚀"
    case ms < 200:
        return "🛰️"
    default:
        return "🐢"
    }
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: go run ./src/main.go <url1> <url2> ...")
        os.Exit(1)
    }
    urls := os.Args[1:]
    resultsCh := make(chan pingResult, len(urls))
    ctx := context.Background()

    for _, raw := range urls {
        // Ensure the URL has a scheme.
        url := raw
        if !strings.HasPrefix(url, "http://") && !strings.HasPrefix(url, "https://") {
            url = "https://" + url
        }
        go func(u string) {
            dur, err := pingHost(ctx, u)
            resultsCh <- pingResult{URL: u, Duration: dur, Err: err}
        }(url)
    }

    var results []pingResult
    for i := 0; i < len(urls); i++ {
        results = append(results, <-resultsCh)
    }

    // Sort by duration (fastest first). Errors are placed at the end.
    sort.SliceStable(results, func(i, j int) bool {
        if results[i].Err != nil {
            return false
        }
        if results[j].Err != nil {
            return true
        }
        return results[i].Duration < results[j].Duration
    })

    for _, r := range results {
        host := r.URL
        // Strip scheme for nicer output.
        host = strings.TrimPrefix(host, "https://")
        host = strings.TrimPrefix(host, "http://")
        if r.Err != nil {
            fmt.Printf("💥 %s error: %v\n", host, r.Err)
            continue
        }
        fmt.Printf("%s %s responded in %dms\n", emojiForDuration(r.Duration), host, r.Duration.Milliseconds())
    }
}
