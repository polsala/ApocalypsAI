package main

import (
    "net/http"
    "net/http/httptest"
    "sync"
    "testing"
    "time"
)

func TestRadiationLevel(t *testing.T) {
    cases := []struct {
        dur      time.Duration
        expected string
    }{
        {50 * time.Millisecond, "⚡️"},
        {150 * time.Millisecond, "☢️"},
        {500 * time.Millisecond, "☣️"},
        {1200 * time.Millisecond, "☠️"},
    }
    for _, c := range cases {
        emoji, _ := radiationLevel(c.dur)
        if emoji != c.expected {
            t.Fatalf("radiationLevel(%v) = %s; want %s", c.dur, emoji, c.expected)
        }
    }
}

func TestBar(t *testing.T) {
    // 0ms -> empty bar, 1000ms -> full bar
    cases := []struct {
        dur      time.Duration
        filled   int // number of █ characters expected
    }{
        {0 * time.Millisecond, 0},
        {250 * time.Millisecond, 2},
        {500 * time.Millisecond, 5},
        {1000 * time.Millisecond, 10},
        {1500 * time.Millisecond, 10}, // capped at full
    }
    for _, c := range cases {
        b := bar(c.dur)
        count := 0
        for _, ch := range b {
            if ch == '█' {
                count++
            }
        }
        if count != c.filled {
            t.Fatalf("bar(%v) has %d filled; want %d", c.dur, count, c.filled)
        }
        if len(b) != 10 {
            t.Fatalf("bar length is %d; want 10", len(b))
        }
    }
}

func TestFetch(t *testing.T) {
    // Mock server that sleeps for 150ms then returns 200 OK.
    srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(150 * time.Millisecond)
        w.WriteHeader(http.StatusOK)
        w.Write([]byte("ok"))
    }))
    defer srv.Close()

    var wg sync.WaitGroup
    ch := make(chan result, 1)
    wg.Add(1)
    go fetch(srv.URL, &wg, ch)
    wg.Wait()
    close(ch)
    res := <-ch
    if res.err != nil {
        t.Fatalf("fetch returned error: %v", res.err)
    }
    // Expect latency around 150ms (allow some jitter).
    if res.latency < 140*time.Millisecond || res.latency > 300*time.Millisecond {
        t.Fatalf("unexpected latency: %v", res.latency)
    }
}
