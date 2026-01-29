package main

import (
    "net/http"
    "net/http/httptest"
    "testing"
    "time"
)

func TestPingSuccess(t *testing.T) {
    // Mock server that responds instantly
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
    }))
    defer server.Close()

    res := ping(server.URL)
    if res.Err != nil {
        t.Fatalf("expected no error, got %v", res.Err)
    }
    if res.Latency > 50*time.Millisecond {
        t.Fatalf("expected latency <50ms, got %v", res.Latency)
    }
}

func TestPingError(t *testing.T) {
    // Invalid URL to force an error
    res := ping("http://127.0.0.1:0")
    if res.Err == nil {
        t.Fatalf("expected error, got nil")
    }
}

func TestStatusMessage(t *testing.T) {
    cases := []struct {
        dur  time.Duration
        want string
    }{
        {10 * time.Millisecond, "Radiant"},
        {150 * time.Millisecond, "Flickering"},
        {500 * time.Millisecond, "Dim"},
    }
    for _, c := range cases {
        got := statusMessage(c.dur)
        if got != c.want {
            t.Errorf("statusMessage(%v) = %s; want %s", c.dur, got, c.want)
        }
    }
}
