package main

import (
    "fmt"
    "io"
    "net/http"
    "os"
    "sort"
    "sync"
    "time"
)

type result struct {
    url     string
    latency time.Duration
    err     error
}

func fetch(url string, wg *sync.WaitGroup, ch chan<- result) {
    defer wg.Done()
    start := time.Now()
    client := http.Client{Timeout: 10 * time.Second}
    resp, err := client.Get(url)
    if err == nil {
        // Drain body to completion
        _, _ = io.Copy(io.Discard, resp.Body)
        resp.Body.Close()
    }
    elapsed := time.Since(start)
    ch <- result{url: url, latency: elapsed, err: err}
}

func radiationLevel(latency time.Duration) (string, string) {
    ms := latency.Milliseconds()
    switch {
    case ms < 100:
        return "⚡️", "Low radiation"
    case ms < 300:
        return "☢️", "Moderate radiation"
    case ms < 700:
        return "☣️", "High radiation"
    default:
        return "☠️", "Critical radiation"
    }
}

func bar(latency time.Duration) string {
    // Max bar length is 10 characters; 1 second maps to a full bar.
    max := 1000.0 // milliseconds
    proportion := float64(latency.Milliseconds()) / max
    if proportion > 1 {
        proportion = 1
    }
    filled := int(proportion * 10)
    bar := ""
    for i := 0; i < filled; i++ {
        bar += "█"
    }
    for i := filled; i < 10; i++ {
        bar += " "
    }
    return bar
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: go run src/main.go <url1> <url2> ...")
        os.Exit(1)
    }
    urls := os.Args[1:]

    var wg sync.WaitGroup
    ch := make(chan result, len(urls))

    for _, u := range urls {
        wg.Add(1)
        go fetch(u, &wg, ch)
    }
    wg.Wait()
    close(ch)

    var results []result
    for r := range ch {
        results = append(results, r)
    }

    sort.Slice(results, func(i, j int) bool {
        return results[i].latency < results[j].latency
    })

    for _, r := range results {
        if r.err != nil {
            fmt.Printf("❌ %s  error: %v\n", r.url, r.err)
            continue
        }
        emoji, level := radiationLevel(r.latency)
        fmt.Printf("%s %s  %dms  [%s] %s\n", emoji, r.url, r.latency.Milliseconds(), bar(r.latency), level)
    }
}
