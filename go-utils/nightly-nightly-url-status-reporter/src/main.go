package main

import (
    "encoding/json"
    "flag"
    "fmt"
    "io/ioutil"
    "net/http"
    "os"
    "strings"
    "sync"
)

type HTTPClient interface {
    Do(req *http.Request) (*http.Response, error)
}

var defaultClient HTTPClient = &http.Client{}

func fetchURL(client HTTPClient, url string) (int, error) {
    req, err := http.NewRequest("HEAD", url, nil)
    if err != nil {
        return 0, err
    }
    resp, err := client.Do(req)
    if err != nil {
        return 0, err
    }
    defer resp.Body.Close()
    return resp.StatusCode, nil
}

func main() {
    urlsFlag := flag.String("urls", "", "Comma separated list of URLs")
    fileFlag := flag.String("file", "", "Path to file containing URLs (one per line)")
    flag.Parse()

    var urls []string
    if *urlsFlag != "" {
        urls = strings.Split(*urlsFlag, ",")
    } else if *fileFlag != "" {
        data, err := ioutil.ReadFile(*fileFlag)
        if err != nil {
            fmt.Fprintf(os.Stderr, "Error reading file: %v\n", err)
            os.Exit(1)
        }
        for _, line := range strings.Split(string(data), "\n") {
            line = strings.TrimSpace(line)
            if line != "" {
                urls = append(urls, line)
            }
        }
    } else {
        fmt.Fprintln(os.Stderr, "Either -urls or -file must be provided")
        os.Exit(1)
    }

    results := make(map[string]int)
    var mu sync.Mutex
    var wg sync.WaitGroup

    for _, u := range urls {
        wg.Add(1)
        go func(url string) {
            defer wg.Done()
            code, err := fetchURL(defaultClient, url)
            mu.Lock()
            defer mu.Unlock()
            if err != nil {
                results[url] = 0
            } else {
                results[url] = code
            }
        }(u)
    }
    wg.Wait()

    out, _ := json.MarshalIndent(results, "", "  ")
    fmt.Println(string(out))
}
