package main

import (
    "errors"
    "flag"
    "fmt"
    "net/http"
    "os"
    "sync"
    "time"
)

type Result struct {
    URL      string
    Latency  time.Duration
    Level    string
    Err      error
}

// mapLatencyToLevel converts latency to a whimsical radiation level.
func mapLatencyToLevel(d time.Duration) string {
    ms := d.Milliseconds()
    switch {
    case ms < 100:
        return "Low"
    case ms <= 300:
        return "Medium"
    default:
        return "High"
    }
}

// pingURL performs a single HTTP GET request and measures latency.
func pingURL(url string) Result {
    start := time.Now()
    resp, err := http.Get(url)
    if err != nil {
        return Result{URL: url, Err: err}
    }
    // Drain body to completion to get accurate timing.
    _, _ = http.ReadResponse(resp.Body, resp.Request)
    resp.Body.Close()
    latency := time.Since(start)
    level := mapLatencyToLevel(latency)
    return Result{URL: url, Latency: latency, Level: level}
}

// worker reads URLs from the jobs channel, pings them, and sends results.
func worker(jobs <-chan string, results chan<- Result, wg *sync.WaitGroup) {
    defer wg.Done()
    for url := range jobs {
        results <- pingURL(url)
    }
}

// pingURLs concurrently pings a slice of URLs and returns ordered results.
func pingURLs(urls []string, maxWorkers int) []Result {
    jobs := make(chan string, len(urls))
    results := make(chan Result, len(urls))
    var wg sync.WaitGroup
    if maxWorkers <= 0 {
        maxWorkers = 5
    }
    for i := 0; i < maxWorkers; i++ {
        wg.Add(1)
        go worker(jobs, results, &wg)
    }
    for _, u := range urls {
        jobs <- u
    }
    close(jobs)
    wg.Wait()
    close(results)
    // Preserve input order for nicer output.
    ordered := make([]Result, len(urls))
    indexMap := make(map[string]int)
    for i, u := range urls {
        indexMap[u] = i
    }
    for r := range results {
        if idx, ok := indexMap[r.URL]; ok {
            ordered[idx] = r
        }
    }
    return ordered
}

func main() {
    maxWorkers := flag.Int("workers", 5, "maximum concurrent workers")
    flag.Parse()
    urls := flag.Args()
    if len(urls) == 0 {
        fmt.Fprintln(os.Stderr, "Usage: radiation-ping [--workers N] <url1> <url2> ...")
        os.Exit(1)
    }
    results := pingURLs(urls, *maxWorkers)
    for _, r := range results {
        if r.Err != nil {
            fmt.Printf("%s\terror: %v\n", r.URL, r.Err)
            continue
        }
        fmt.Printf("%s\t%v\t%s\n", r.URL, r.Latency, r.Level)
    }
}
