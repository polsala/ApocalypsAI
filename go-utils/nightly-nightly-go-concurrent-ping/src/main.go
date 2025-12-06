package main

import (
    "bufio"
    "flag"
    "fmt"
    "net/http"
    "os"
    "sort"
    "strings"
    "sync"
    "time"
)

func pingURL(url string) string {
    client := http.Client{
        Timeout: 5 * time.Second,
    }
    resp, err := client.Get(url)
    if err != nil {
        return fmt.Sprintf("%s -> error: %s", url, err.Error())
    }
    defer resp.Body.Close()
    return fmt.Sprintf("%s -> %d", url, resp.StatusCode)
}

// PingURLs reads URLs from filePath, pings them with max concurrency, and returns sorted results.
func PingURLs(filePath string, concurrency int) ([]string, error) {
    file, err := os.Open(filePath)
    if err != nil {
        return nil, err
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    var urls []string
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line != "" {
            urls = append(urls, line)
        }
    }
    if err := scanner.Err(); err != nil {
        return nil, err
    }

    if concurrency <= 0 {
        concurrency = 10
    }
    sem := make(chan struct{}, concurrency)
    var wg sync.WaitGroup
    var mu sync.Mutex
    results := make([]string, 0, len(urls))

    for _, u := range urls {
        wg.Add(1)
        go func(url string) {
            defer wg.Done()
            sem <- struct{}{}
            res := pingURL(url)
            mu.Lock()
            results = append(results, res)
            mu.Unlock()
            <-sem
        }(u)
    }
    wg.Wait()
    sort.Strings(results)
    return results, nil
}

func main() {
    filePath := flag.String("file", "", "Path to file containing URLs (one per line)")
    concurrency := flag.Int("concurrency", 10, "Maximum concurrent requests")
    flag.Parse()

    if *filePath == "" {
        fmt.Fprintln(os.Stderr, "error: -file is required")
        os.Exit(1)
    }

    results, err := PingURLs(*filePath, *concurrency)
    if err != nil {
        fmt.Fprintln(os.Stderr, "error:", err)
        os.Exit(1)
    }
    for _, line := range results {
        fmt.Println(line)
    }
}
