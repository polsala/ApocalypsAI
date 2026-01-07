package main

import (
    "errors"
    "reflect"
    "testing"
    "time"
)

// mockPing returns predefined latencies or errors based on the host name.
func mockPingFactory(map[string]struct {
    dur time.Duration
    err error
}) pingFunc {
    return func(host string, timeout time.Duration) (time.Duration, error) {
        if v, ok := map[host]; ok {
            return v.dur, v.err
        }
        return 0, errors.New("unknown host")
    }
}

func TestPingHostSuccess(t *testing.T) {
    pf := mockPingFactory(map[string]struct {
        dur time.Duration
        err error
    }{
        "fast.example.com": {dur: 42 * time.Millisecond, err: nil},
    })
    res := pingHost("fast.example.com", 1*time.Second, pf)
    if res.Error != "" {
        t.Fatalf("expected no error, got %s", res.Error)
    }
    if res.LatencyMs != 42 {
        t.Fatalf("expected latency 42ms, got %d", res.LatencyMs)
    }
}

func TestPingHostError(t *testing.T) {
    pf := mockPingFactory(map[string]struct {
        dur time.Duration
        err error
    }{
        "down.example.com": {dur: 0, err: errors.New("dial timeout")},
    })
    res := pingHost("down.example.com", 1*time.Second, pf)
    if res.Error != "dial timeout" {
        t.Fatalf("expected error 'dial timeout', got %s", res.Error)
    }
    if res.LatencyMs != 0 {
        t.Fatalf("expected latency 0 on error, got %d", res.LatencyMs)
    }
}

func TestRunPingsDeterministic(t *testing.T) {
    hosts := []string{"a.example.com", "b.example.com", "c.example.com"}
    pf := mockPingFactory(map[string]struct {
        dur time.Duration
        err error
    }{
        "a.example.com": {dur: 10 * time.Millisecond, err: nil},
        "b.example.com": {dur: 0, err: errors.New("dial timeout")},
        "c.example.com": {dur: 30 * time.Millisecond, err: nil},
    })
    results := runPings(hosts, 2, 1*time.Second, pf)
    // Convert slice to map for order‑independent verification.
    got := make(map[string]Result)
    for _, r := range results {
        got[r.Host] = r
    }
    expected := map[string]Result{
        "a.example.com": {Host: "a.example.com", LatencyMs: 10},
        "b.example.com": {Host: "b.example.com", Error: "dial timeout"},
        "c.example.com": {Host: "c.example.com", LatencyMs: 30},
    }
    if !reflect.DeepEqual(got, expected) {
        t.Fatalf("unexpected results.\nGot:  %#v\nWant: %#v", got, expected)
    }
}
