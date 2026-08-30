package main

import (
    "net/http"
    "net/http/httptest"
    "testing"
    "time"
)

func TestPingURLSuccess(t *testing.T) {
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
    }))
    defer server.Close()
    client := &http.Client{Timeout: 1 * time.Second}
    res := pingURL(client, server.URL)
    if res.err != nil {
        t.Fatalf("expected no error, got %v", res.err)
    }
    if res.duration > 200*time.Millisecond {
        t.Fatalf("expected quick response, got %v", res.duration)
    }
}

func TestPingURLTimeout(t *testing.T) {
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(200 * time.Millisecond)
        w.WriteHeader(http.StatusOK)
    }))
    defer server.Close()
    client := &http.Client{Timeout: 100 * time.Millisecond}
    res := pingURL(client, server.URL)
    if res.err == nil {
        t.Fatalf("expected timeout error, got nil")
    }
    // Mock rationale: we only verify that an error occurred, not its exact type.
}
