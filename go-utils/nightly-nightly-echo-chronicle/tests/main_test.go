package main

import (
    "net/http"
    "net/http/httptest"
    "sync"
    "testing"
    "time"
)

func TestPingDurations(t *testing.T) {
    // Mock server 1: 50ms delay
    srv1 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(50 * time.Millisecond)
        w.WriteHeader(http.StatusOK)
        w.Write([]byte("ok"))
    }))
    defer srv1.Close()

    // Mock server 2: 100ms delay
    srv2 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(100 * time.Millisecond)
        w.WriteHeader(http.StatusOK)
        w.Write([]byte("ok"))
    }))
    defer srv2.Close()

    urls := []string{srv1.URL, srv2.URL}
    var wg sync.WaitGroup
    ch := make(chan result, len(urls))

    for _, u := range urls {
        wg.Add(1)
        go ping(u, &wg, ch)
    }
    wg.Wait()
    close(ch)

    results := make(map[string]time.Duration)
    for r := range ch {
        if r.err != nil {
            t.Fatalf("unexpected error for %s: %v", r.url, r.err)
        }
        results[r.url] = r.duration
    }

    // Verify that durations are within expected bounds (+20ms tolerance)
    if d, ok := results[srv1.URL]; ok {
        if d < 50*time.Millisecond || d > 80*time.Millisecond {
            t.Errorf("srv1 duration out of bounds: %v", d)
        }
    } else {
        t.Errorf("result for srv1 missing")
    }

    if d, ok := results[srv2.URL]; ok {
        if d < 100*time.Millisecond || d > 130*time.Millisecond {
            t.Errorf("srv2 duration out of bounds: %v", d)
        }
    } else {
        t.Errorf("result for srv2 missing")
    }
}
