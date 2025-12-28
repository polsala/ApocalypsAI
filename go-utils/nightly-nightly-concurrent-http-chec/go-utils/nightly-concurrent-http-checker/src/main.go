package main

import (
    \"flag\"
    \"fmt\"
    \"net/http\"
    \"sync\"
    \"time\"
)

type result struct {
    url    string
    status int
    err    error
}

func checkURL(url string, client *http.Client, resCh chan<- result, wg *sync.WaitGroup) {
    defer wg.Done()
    resp, err := client.Get(url)
    if err != nil {
        resCh <- result{url: url, err: err}
        return
    }
    defer resp.Body.Close()
    resCh <- result{url: url, status: resp.StatusCode}
}

func main() {
    concurrency := flag.Int(\"concurrency\", 5, \"Number of concurrent workers\")
    flag.Parse()
    urls := flag.Args()
    if len(urls) == 0 {
        fmt.Println(\"No URLs provided\")
        return
    }

    client := &http.Client{
        Timeout: 5 * time.Second,
    }

    resCh := make(chan result, len(urls))
    var wg sync.WaitGroup
    sem := make(chan struct{}, *concurrency)

    for _, url := range urls {
        wg.Add(1)
        sem <- struct{}{}
        go func(u string) {
            defer func() { <-sem }()
            checkURL(u, client, resCh, &wg)
        }(url)
    }

    wg.Wait()
    close(resCh)

    for r := range resCh {
        if r.err != nil {
            fmt.Printf(\"URL: %s - Error: %v\\n\", r.url, r.err)
        } else {
            fmt.Printf(\"URL: %s - Status: %d\\n\", r.url, r.status)
        }
    }
}
