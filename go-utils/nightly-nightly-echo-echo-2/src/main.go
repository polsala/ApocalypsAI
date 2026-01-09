package main

import (
    "flag"
    "fmt"
    "net/http"
    "os"
    "sort"
    "sync"
    "time"
)

type Result struct {
    URL      string
    Status   int
    Duration time.Duration
    Err      error
}

func CheckURLs(urls []string, timeout time.Duration, concurrency int) []Result {
    var wg sync.WaitGroup
    sem := make(chan struct{}, concurrency)
    results := make([]Result, len(urls))
    for i, url := range urls {
        wg.Add(1)
        go func(idx int, u string) {
            defer wg.Done()
            sem <- struct{}{}
            defer func() { <-sem }()
            client := &http.Client{Timeout: timeout}
            start := time.Now()
            resp, err := client.Get(u)
            duration := time.Since(start)
            if err != nil {
                results[idx] = Result{URL: u, Err: err}
                return
            }
            defer resp.Body.Close()
            results[idx] = Result{URL: u, Status: resp.StatusCode, Duration: duration}
        }(i, url)
    }
    wg.Wait()
    return results
}

func emojiForResult(r Result) string {
    if r.Err != nil {
        if os.IsTimeout(r.Err) || r.Err.Error() == "Client.Timeout exceeded while awaiting headers" {
            return "⏳"
        }
        return "❌"
    }
    if r.Status >= 200 && r.Status < 300 {
        return "✅"
    }
    return "❌"
}

func main() {
    timeoutFlag := flag.Int("t", 5, "timeout in seconds per request")
    concurrencyFlag := flag.Int("c", 10, "maximum concurrent requests")
    flag.Parse()
    urls := flag.Args()
    if len(urls) == 0 {
        fmt.Println("Usage: nightly-echo-echo [-t timeout] [-c concurrency] url1 url2 ...")
        os.Exit(1)
    }
    timeout := time.Duration(*timeoutFlag) * time.Second
    concurrency := *concurrencyFlag
    results := CheckURLs(urls, timeout, concurrency)
    sort.Slice(results, func(i, j int) bool { return results[i].URL < results[j].URL })
    for _, r := range results {
        if r.Err != nil {
            if os.IsTimeout(r.Err) || r.Err.Error() == "Client.Timeout exceeded while awaiting headers" {
                fmt.Printf("%s %s (timeout after %ds)\n", emojiForResult(r), r.URL, int(timeout.Seconds()))
            } else {
                fmt.Printf("%s %s (%v)\n", emojiForResult(r), r.URL, r.Err)
            }
            continue
        }
        fmt.Printf("%s %s (%d) %.1fms\n", emojiForResult(r), r.URL, r.Status, float64(r.Duration.Microseconds())/1000.0)
    }
}
