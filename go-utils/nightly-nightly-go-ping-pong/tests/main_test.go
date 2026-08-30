package main

import (
    "errors"
    "sync"
    "testing"
    "time"
)

func TestCategorize(t *testing.T) {
    cases := []struct {
        dur  time.Duration
        want string
    }{
        {10 * time.Millisecond, "🐇 Lightning rabbit"},
        {100 * time.Millisecond, "🐦 Swift sparrow"},
        {250 * time.Millisecond, "🐢 Steady turtle"},
        {500 * time.Millisecond, "🐌 Slothful snail"},
    }
    for _, c := range cases {
        got := categorize(c.dur)
        if got != c.want {
            t.Errorf("categorize(%v) = %s; want %s", c.dur, got, c.want)
        }
    }
}

func TestPingHost_MockSuccess(t *testing.T) {
    // Replace pingFunc with a deterministic mock.
    pingFunc = func(host string) (time.Duration, error) {
        if host == "fast.example.com" {
            return 30 * time.Millisecond, nil
        }
        return 0, errors.New("unreachable")
    }
    defer func() { pingFunc = realPing }() // restore after test

    out := make(chan pingResult, 1)
    var wg sync.WaitGroup
    wg.Add(1)
    go pingHost("fast.example.com", &wg, out)
    wg.Wait()
    close(out)
    res := <-out
    if res.err != nil {
        t.Fatalf("expected no error, got %v", res.err)
    }
    if res.latency != 30*time.Millisecond {
        t.Fatalf("expected 30ms latency, got %v", res.latency)
    }
    if got := categorize(res.latency); got != "🐇 Lightning rabbit" {
        t.Fatalf("unexpected category: %s", got)
    }
}
