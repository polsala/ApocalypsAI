package main

import (
    "errors"
    "net/http"
    "net/http/httptest"
    "testing"
    "time"
)

func TestCategorize(t *testing.T) {
    cases := []struct {
        name     string
        latency  time.Duration
        err      error
        expected string
    }{
        {"Radiant", 50 * time.Millisecond, nil, "Radiant"},
        {"Stable", 150 * time.Millisecond, nil, "Stable"},
        {"Fading", 400 * time.Millisecond, nil, "Fading"},
        {"Lost", 0, errors.New("timeout"), "Lost"},
    }

    for _, c := range cases {
        t.Run(c.name, func(t *testing.T) {
            got := categorize(c.latency, c.err)
            if got != c.expected {
                t.Fatalf("expected %s, got %s", c.expected, got)
            }
        })
    }
}

// Mock rationale: use httptest server to simulate latency without real network.
func TestPingURL(t *testing.T) {
    srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(120 * time.Millisecond)
        w.WriteHeader(http.StatusOK)
    }))
    defer srv.Close()

    lat, err := pingURL(srv.URL, 2*time.Second)
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if lat < 110*time.Millisecond || lat > 150*time.Millisecond {
        t.Fatalf("latency out of expected range: %v", lat)
    }
}
