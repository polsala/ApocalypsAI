package main

import (
    "context"
    "net/http"
    "net/http/httptest"
    "testing"
    "time"
)

// mockServer returns an httptest.Server that waits for the specified delay before responding.
func mockServer(delay time.Duration) *httptest.Server {
    handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(delay)
        w.WriteHeader(http.StatusOK)
        _, _ = w.Write([]byte("ok"))
    })
    return httptest.NewServer(handler)
}

func TestPingHostFast(t *testing.T) {
    srv := mockServer(10 * time.Millisecond)
    defer srv.Close()

    ctx := context.Background()
    dur, err := pingHost(ctx, srv.URL)
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    // Allow a small tolerance for scheduling overhead.
    if dur > 30*time.Millisecond {
        t.Fatalf("expected duration <30ms, got %v", dur)
    }
}

func TestPingHostSlow(t *testing.T) {
    srv := mockServer(150 * time.Millisecond)
    defer srv.Close()

    ctx := context.Background()
    dur, err := pingHost(ctx, srv.URL)
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if dur < 120*time.Millisecond || dur > 200*time.Millisecond {
        t.Fatalf("expected duration around 150ms, got %v", dur)
    }
}

func TestPingHostError(t *testing.T) {
    // Use an invalid URL to trigger an error.
    ctx := context.Background()
    _, err := pingHost(ctx, "http://invalid.invalid")
    if err == nil {
        t.Fatalf("expected an error for invalid host, got nil")
    }
}
