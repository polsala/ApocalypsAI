package main

import (
    "encoding/json"
    "fmt"
    "net/http"
    "os"
    "sync"
)

// fetchStatuses concurrently GETs each URL and records the HTTP status code.
// If a request fails, the status code is recorded as 0.
func fetchStatuses(urls []string) map[string]int {
    results := make(map[string]int)
    var mu sync.Mutex
    var wg sync.WaitGroup
    client := &http.Client{}
    for _, u := range urls {
        wg.Add(1)
        go func(url string) {
            defer wg.Done()
            resp, err := client.Get(url)
            status := 0
            if err == nil {
                status = resp.StatusCode
                resp.Body.Close()
            }
            mu.Lock()
            results[url] = status
            mu.Unlock()
        }(u)
    }
    wg.Wait()
    return results
}

func main() {
    if len(os.Args) < 2 {
        fmt.Fprintln(os.Stderr, "Usage: chrononaut-ping <url1> <url2> ...")
        os.Exit(1)
    }
    urls := os.Args[1:]
    statuses := fetchStatuses(urls)
    out, err := json.Marshal(statuses)
    if err != nil {
        fmt.Fprintln(os.Stderr, "Error marshaling JSON:", err)
        os.Exit(1)
    }
    fmt.Println(string(out))
}
