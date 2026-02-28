package main

import (
    "bufio"
    "flag"
    "fmt"
    "net/http"
    "os"
    "strings"
    "sync"
    "time"
)

const (
    timeoutSeconds = 5
    // ANSI color codes
    colorReset  = "\u001b[0m"
    colorGreen  = "\u001b[32m"
    colorRed    = "\u001b[31m"
)

// checkURL performs an HTTP GET with a timeout and returns a formatted status string.
func checkURL(url string, timeout time.Duration) string {
    client := http.Client{Timeout: timeout}
    resp, err := client.Get(url)
    if err != nil {
        return fmt.Sprintf("%s☢️ %s timed out after %ds%s", colorRed, url, int(timeout.Seconds()), colorReset)
    }
    defer resp.Body.Close()
    return fmt.Sprintf("%s✅ %s responded with %d %s%s", colorGreen, url, resp.StatusCode, http.StatusText(resp.StatusCode), colorReset)
}

// loadURLsFromFile reads a file line‑by‑line, ignoring empty lines and comments.
func loadURLsFromFile(path string) ([]string, error) {
    f, err := os.Open(path)
    if err != nil {
        return nil, err
    }
    defer f.Close()

    var urls []string
    scanner := bufio.NewScanner(f)
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line == "" || strings.HasPrefix(line, "#") {
            continue
        }
        urls = append(urls, line)
    }
    return urls, scanner.Err()
}

func main() {
    filePath := flag.String("file", "", "Path to a file containing one URL per line")
    flag.Parse()

    var urls []string
    if *filePath != "" {
        fUrls, err := loadURLsFromFile(*filePath)
        if err != nil {
            fmt.Fprintf(os.Stderr, "Error reading file %s: %v\n", *filePath, err)
            os.Exit(1)
        }
        urls = append(urls, fUrls...)
    }
    // Remaining command‑line arguments are also treated as URLs.
    urls = append(urls, flag.Args()...)

    if len(urls) == 0 {
        fmt.Fprintln(os.Stderr, "No URLs provided. Use arguments or -file flag.")
        os.Exit(1)
    }

    var wg sync.WaitGroup
    results := make(chan string, len(urls))
    timeout := time.Duration(timeoutSeconds) * time.Second

    for _, u := range urls {
        wg.Add(1)
        go func(url string) {
            defer wg.Done()
            results <- checkURL(url, timeout)
        }(u)
    }

    wg.Wait()
    close(results)

    for r := range results {
        fmt.Println(r)
    }
}
