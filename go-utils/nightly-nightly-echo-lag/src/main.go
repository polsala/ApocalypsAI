package main

import (
    "flag"
    "fmt"
    "net/http"
    "os"
    "sync"
    "time"
)

type Result struct {
    URL        string
    StatusCode int
    Message    string
}

func whimsicalMessage(status int) string {
    switch {
    case status >= 200 && status < 300:
        return "All good!"
    case status == 404:
        return "Lost in the void!"
    case status >= 500 && status < 600:
        return "Server is crying!"
    default:
        return "Mysterious response."
    }
}

func fetchURL(client *http.Client, url string, wg *sync.WaitGroup, ch chan<- Result) {
    defer wg.Done()
    req, err := http.NewRequest("HEAD", url, nil)
    if err != nil {
        ch <- Result{URL: url, StatusCode: 0, Message: fmt.Sprintf("Request error: %v", err)}
        return
    }
    resp, err := client.Do(req)
    if err != nil {
        ch <- Result{URL: url, StatusCode: 0, Message: fmt.Sprintf("Request error: %v", err)}
        return
    }
    defer resp.Body.Close()
    ch <- Result{URL: url, StatusCode: resp.StatusCode, Message: whimsicalMessage(resp.StatusCode)}
}

func main() {
    flag.Usage = func() {
        fmt.Fprintf(flag.CommandLine.Output(), "Usage: %s [URL ...]
", os.Args[0])
        flag.PrintDefaults()
    }
    flag.Parse()
    urls := flag.Args()
    if len(urls) == 0 {
        flag.Usage()
        os.Exit(1)
    }

    client := &http.Client{
        Timeout: 5 * time.Second,
    }

    var wg sync.WaitGroup
    resultsCh := make(chan Result, len(urls))

    for _, url := range urls {
        wg.Add(1)
        go fetchURL(client, url, &wg, resultsCh)
    }

    wg.Wait()
    close(resultsCh)

    for res := range resultsCh {
        fmt.Printf("%s -> %d: %s
", res.URL, res.StatusCode, res.Message)
    }
}
