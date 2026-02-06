package main

import (
    "net/http"
    "net/http/httptest"
    "testing"
    "time"
)

func TestPingURLs(t *testing.T) {
    // Mock server 1: 10ms delay
    srv1 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(10 * time.Millisecond)
        w.WriteHeader(http.StatusOK)
    }))
    defer srv1.Close()

    // Mock server 2: 20ms delay
    srv2 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(20 * time.Millisecond)
        w.WriteHeader(http.StatusOK)
    }))
    defer srv2.Close()

    urls := []string{srv1.URL, srv2.URL}
    results := PingURLs(urls)

    if len(results) != 2 {
        t.Fatalf("expected 2 results, got %d", len(results))
    }

    tolerance := 5 * time.Millisecond // allow small scheduling variance

    // Validate first server (~10ms)
    if results[0].Err != nil {
        t.Errorf("unexpected error for %s: %v", results[0].URL, results[0].Err)
    } else if results[0].Duration < 10*time.Millisecond || results[0].Duration > 10*time.Millisecond+tolerance {
        t.Errorf("expected ~10ms duration for %s, got %v", results[0].URL, results[0].Duration)
    }

    // Validate second server (~20ms)
    if results[1].Err != nil {
        t.Errorf("unexpected error for %s: %v", results[1].URL, results[1].Err)
    } else if results[1].Duration < 20*time.Millisecond || results[1].Duration > 20*time.Millisecond+tolerance {
        t.Errorf("expected ~20ms duration for %s, got %v", results[1].URL, results[1].Duration)
    }
}
