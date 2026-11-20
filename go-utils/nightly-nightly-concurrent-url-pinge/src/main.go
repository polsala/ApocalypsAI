package main

import (
    "bufio"
    "context"
    "flag"
    "fmt"
    "net/http"
    "os"
    "strings"
    "sync"
    "time"
)

// checkURL attempts to GET the given URL with a timeout.
// It returns "UP" if the request succeeds with a 2xx status code, otherwise "DOWN".
func checkURL(url string) string {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return "DOWN"
    }
    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return "DOWN"
    }
    defer resp.Body.Close()
    if resp.StatusCode >= 200 && resp.StatusCode < 300 {
        return "UP"
    }
    return "DOWN"
}

func main() {
    // Parse concurrency flag
    concurrency := flag.Int("c", 5, "maximum concurrent requests")
    flag.Parse()

    // Gather URLs from args or stdin
    var urls []string
    if flag.NArg() > 0 {
        urls = flag.Args()
    } else {
        scanner := bufio.NewScanner(os.Stdin)
        for scanner.Scan() {
            line := strings.TrimSpace(scanner.Text())
            if line != "" {
                urls = append(urls, line)
            }
        }
        if err := scanner.Err(); err != nil {
            fmt.Fprintf(os.Stderr, "error reading stdin: %v\n", err)
            os.Exit(1)
        }
    }

    if len(urls) == 0 {
        fmt.Fprintln(os.Stderr, "no URLs provided")
        os.Exit(1)
    }

    // Semaphore to limit concurrency
    sem := make(chan struct{}, *concurrency)
    var wg sync.WaitGroup
    results := make([]string, len(urls))

    for i, u := range urls {
        wg.Add(1)
        go func(idx int, url string) {
            defer wg.Done()
            sem <- struct{}{} // acquire
            status := checkURL(url)
            results[idx] = fmt.Sprintf("%s %s", url, status)
            <-sem // release
        }(i, u)
    }

    wg.Wait()
    for _, line := range results {
        fmt.Println(line)
    }
}
