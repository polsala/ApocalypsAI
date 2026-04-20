package main

import (
    "net/http"
    "net/http/httptest"
    "testing"
    "time"
)

func TestPingURLs(t *testing.T) {
    // Mock server that responds immediately.
    fast := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
    }))
    defer fast.Close()

    // Mock server that delays its response.
    delayed := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(150 * time.Millisecond)
        w.WriteHeader(http.StatusOK)
    }))
    defer delayed.Close()

    urls := []string{fast.URL, delayed.URL}
    results := pingURLs(urls, 500*time.Millisecond)

    // Verify both URLs were reached.
    if d, ok := results[fast.URL]; !ok || d < 0 {
        t.Fatalf("fast server not reachable or timed out")
    }
    if d, ok := results[delayed.URL]; !ok || d < 0 {
        t.Fatalf("delayed server not reachable or timed out")
    }

    // Ensure the delayed server reports a higher latency than the fast one.
    if results[delayed.URL] <= results[fast.URL] {
        t.Fatalf("expected delayed latency > fast latency")
    }
}
