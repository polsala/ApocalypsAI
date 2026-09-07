package main

import (
    "fmt"
    "testing"
    "time"
)

func TestRunPings_Mocked(t *testing.T) {
    // Save original PingFunc and restore after test.
    original := PingFunc
    defer func() { PingFunc = original }()

    // Mock implementation returning deterministic latencies.
    PingFunc = func(host string) (time.Duration, error) {
        switch host {
        case "fast.com":
            return 10 * time.Millisecond, nil
        case "slow.com":
            return 1500 * time.Millisecond, nil
        case "down.com":
            return 0, fmt.Errorf("timeout")
        default:
            return 0, fmt.Errorf("unknown host")
        }
    }

    hosts := []string{"fast.com", "slow.com", "down.com"}
    results := runPings(hosts)

    if len(results) != 3 {
        t.Fatalf("expected 3 results, got %d", len(results))
    }

    // Verify each mocked response.
    for _, r := range results {
        switch r.Host {
        case "fast.com":
            if r.Err != nil || r.Latency != 10*time.Millisecond {
                t.Errorf("fast.com expected 10ms latency, got %v, err=%v", r.Latency, r.Err)
            }
        case "slow.com":
            if r.Err != nil || r.Latency != 1500*time.Millisecond {
                t.Errorf("slow.com expected 1500ms latency, got %v, err=%v", r.Latency, r.Err)
            }
        case "down.com":
            if r.Err == nil {
                t.Errorf("down.com expected error, got nil")
            }
        }
    }
}
