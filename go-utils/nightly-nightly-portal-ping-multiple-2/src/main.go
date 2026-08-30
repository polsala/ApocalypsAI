package main

import (
    "bufio"
    "flag"
    "fmt"
    "io"
    "net/http"
    "os"
    "strings"
    "sync"
    "time"
)

type result struct {
    url      string
    duration time.Duration
    err      error
}

func pingURL(client *http.Client, url string) result {
    start := time.Now()
    resp, err := client.Get(url)
    if err == nil {
        // Drain body to completion
        _, _ = io.Copy(io.Discard, resp.Body)
        resp.Body.Close()
    }
    return result{url: url, duration: time.Since(start), err: err}
}

func main() {
    timeout := flag.Duration("timeout", 5*time.Second, "request timeout")
    flag.Parse()
    urls := []string{}
    // URLs from positional arguments
    for _, arg := range flag.Args() {
        urls = append(urls, arg)
    }
    // If no args, read from stdin (one URL per line)
    if len(urls) == 0 {
        scanner := bufio.NewScanner(os.Stdin)
        for scanner.Scan() {
            line := strings.TrimSpace(scanner.Text())
            if line != "" {
                urls = append(urls, line)
            }
        }
    }
    if len(urls) == 0 {
        fmt.Fprintln(os.Stderr, "No URLs provided")
        os.Exit(1)
    }

    client := &http.Client{Timeout: *timeout}
    var wg sync.WaitGroup
    resultsCh := make(chan result, len(urls))

    for _, u := range urls {
        wg.Add(1)
        go func(url string) {
            defer wg.Done()
            resultsCh <- pingURL(client, url)
        }(u)
    }
    wg.Wait()
    close(resultsCh)

    var success int
    var total time.Duration
    fmt.Println("Portal Ping Results:")
    for r := range resultsCh {
        if r.err != nil {
            fmt.Printf("- %s : ✖ %v\n", r.url, r.err)
        } else {
            fmt.Printf("- %s : ✔ %d ms\n", r.url, r.duration.Milliseconds())
            success++
            total += r.duration
        }
    }
    fmt.Printf("\nSummary: %d/%d successful, average latency %.2f ms\n", success, len(urls), func() float64 {
        if success == 0 {
            return 0
        }
        return float64(total.Milliseconds()) / float64(success)
    }())
}
