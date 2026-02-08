package main

import (
    "net/http"
    "net/http/httptest"
    "testing"
    "time"
)

// Mock rationale: deterministic server always returns 200 OK instantly.
func TestRunSingleServer(t *testing.T) {
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
    }))
    defer server.Close()

    urls := []string{server.URL}
    stats := run(urls, 2, 200*time.Millisecond)

    if stats.Total == 0 {
        t.Fatalf("expected at least one request, got 0")
    }
    if stats.Failure != 0 {
        t.Fatalf("expected zero failures, got %d", stats.Failure)
    }
    if stats.Success == 0 {
        t.Fatalf("expected some successful requests, got 0")
    }
}
