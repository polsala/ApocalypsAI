package main

import (
    "errors"
    "testing"
    "time"
)

func TestPingConcurrently(t *testing.T) {
    // Mock Ping function to avoid real network calls
    Ping = func(host string) (time.Duration, error) {
        switch host {
        case "fast.example":
            return 50 * time.Millisecond, nil
        case "slow.example":
            return 500 * time.Millisecond, nil
        case "down.example":
            return 0, errors.New("connection refused")
        default:
            return 0, errors.New("unknown host")
        }
    }
    // Restore the original Ping after the test
    defer func() { Ping = defaultPing }()

    hosts := []string{"fast.example", "slow.example", "down.example"}
    results := pingConcurrently(hosts)

    if len(results) != 3 {
        t.Fatalf("expected 3 results, got %d", len(results))
    }

    for _, r := range results {
        switch r.Host {
        case "fast.example":
            if r.Err != nil || r.Latency != 50*time.Millisecond {
                t.Errorf("fast host unexpected result: latency=%v err=%v", r.Latency, r.Err)
            }
        case "slow.example":
            if r.Err != nil || r.Latency != 500*time.Millisecond {
                t.Errorf("slow host unexpected result: latency=%v err=%v", r.Latency, r.Err)
            }
        case "down.example":
            if r.Err == nil {
                t.Errorf("down host expected an error, got nil")
            }
        }
    }
}
