package main

import (
    "net/http"
    "sync"
    "testing"
)

type mockClient struct {
    responses map[string]int
}

func (m *mockClient) Do(req *http.Request) (*http.Response, error) {
    code, ok := m.responses[req.URL.String()]
    if !ok {
        return &http.Response{StatusCode: 0, Body: http.NoBody}, nil
    }
    return &http.Response{StatusCode: code, Body: http.NoBody}, nil
}

func TestFetchURL(t *testing.T) {
    mock := &mockClient{responses: map[string]int{
        "https://example.com": 200,
        "https://bad.com":     404,
    }}
    code, err := fetchURL(mock, "https://example.com")
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if code != 200 {
        t.Fatalf("expected 200, got %d", code)
    }

    code, err = fetchURL(mock, "https://bad.com")
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if code != 404 {
        t.Fatalf("expected 404, got %d", code)
    }

    code, err = fetchURL(mock, "https://unknown.com")
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if code != 0 {
        t.Fatalf("expected 0 for unknown, got %d", code)
    }
}

func TestConcurrentFetch(t *testing.T) {
    mock := &mockClient{responses: map[string]int{
        "https://a.com": 200,
        "https://b.com": 404,
    }}
    urls := []string{"https://a.com", "https://b.com"}
    results := make(map[string]int)
    var mu sync.Mutex
    var wg sync.WaitGroup

    for _, u := range urls {
        wg.Add(1)
        go func(url string) {
            defer wg.Done()
            code, _ := fetchURL(mock, url)
            mu.Lock()
            results[url] = code
            mu.Unlock()
        }(u)
    }
    wg.Wait()

    if results["https://a.com"] != 200 {
        t.Errorf("expected 200 for a.com, got %d", results["https://a.com"])
    }
    if results["https://b.com"] != 404 {
        t.Errorf("expected 404 for b.com, got %d", results["https://b.com"])
    }
}
