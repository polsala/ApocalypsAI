package main

import (
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "os"
)

type Quote struct {
    Content string `json:"content"`
    Author  string `json:"author"`
}

func fetchQuote(url string) (*Quote, error) {
    resp, err := http.Get(url)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    if resp.StatusCode != http.StatusOK {
        return nil, fmt.Errorf("unexpected status: %s", resp.Status)
    }
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }
    var q Quote
    if err := json.Unmarshal(body, &q); err != nil {
        return nil, err
    }
    return &q, nil
}

func main() {
    url := "https://api.quotable.io/random"
    q, err := fetchQuote(url)
    if err != nil {
        fmt.Fprintf(os.Stderr, "Error fetching quote: %v\n", err)
        os.Exit(1)
    }
    fmt.Printf("\"%s\" — %s\n", q.Content, q.Author)
}
