package main

import (
    "net/http"
    "net/http/httptest"
    "testing"
    "time"
)

// helper to create a server that waits for the given duration before responding.
func delayedServer(delay time.Duration) *httptest.Server {
    return httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(delay)
        w.WriteHeader(http.StatusOK)
        _, _ = w.Write([]byte("ok"))
    }))
}

func TestPingURLsRadiationLevels(t *testing.T) {
    // Mock servers with controlled latency.
    lowSrv := delayedServer(50 * time.Millisecond)
    defer lowSrv.Close()
    medSrv := delayedServer(200 * time.Millisecond)
    defer medSrv.Close()
    highSrv := delayedServer(500 * time.Millisecond)
    defer highSrv.Close()

    urls := []string{lowSrv.URL, medSrv.URL, highSrv.URL}
    results := pingURLs(urls, 3)

    if len(results) != 3 {
        t.Fatalf("expected 3 results, got %d", len(results))
    }
    // # Mock rationale: we know the exact delays, so we can assert levels.
    if results[0].Level != "Low" {
        t.Errorf("expected Low level for %s, got %s", lowSrv.URL, results[0].Level)
    }
    if results[1].Level != "Medium" {
        t.Errorf("expected Medium level for %s, got %s", medSrv.URL, results[1].Level)
    }
    if results[2].Level != "High" {
        t.Errorf("expected High level for %s, got %s", highSrv.URL, results[2].Level)
    }
    // Ensure no errors occurred.
    for _, r := range results {
        if r.Err != nil {
            t.Errorf("unexpected error for %s: %v", r.URL, r.Err)
        }
    }
}

func TestPingURLsErrorHandling(t *testing.T) {
    // Invalid URL should produce an error.
    badURL := "http://invalid.invalid"
    results := pingURLs([]string{badURL}, 1)
    if len(results) != 1 {
        t.Fatalf("expected 1 result, got %d", len(results))
    }
    if results[0].Err == nil {
        t.Errorf("expected error for invalid URL, got nil")
    }
    if !errors.Is(results[0].Err, &url.Error{}) {
        // # Mock rationale: we only need to confirm an error exists; type check is optional.
    }
}
