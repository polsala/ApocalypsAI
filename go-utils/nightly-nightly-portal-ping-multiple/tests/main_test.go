package main

import (
    "errors"
    "testing"
    "time"
)

func TestPingAll_Mocked(t *testing.T) {
    // Mock PingFunc to return deterministic results.
    mock := func(host string, timeout time.Duration) (time.Duration, error) {
        switch host {
        case "fast.host":
            return 10 * time.Millisecond, nil
        case "slow.host":
            return 1500 * time.Millisecond, nil
        case "down.host":
            return 0, errors.New("timeout")
        default:
            return 0, errors.New("unknown")
        }
    }
    PingFunc = mock
    defer func() { PingFunc = defaultPing }()

    hosts := []string{"fast.host", "slow.host", "down.host"}
    results := pingAll(hosts, 2*time.Second)

    if len(results) != 3 {
        t.Fatalf("expected 3 results, got %d", len(results))
    }

    // fast.host
    if results[0].Err != nil || results[0].Latency != 10*time.Millisecond {
        t.Errorf("fast.host result mismatch: %+v", results[0])
    }
    // slow.host
    if results[1].Err != nil || results[1].Latency != 1500*time.Millisecond {
        t.Errorf("slow.host result mismatch: %+v", results[1])
    }
    // down.host
    if results[2].Err == nil || results[2].Err.Error() != "timeout" {
        t.Errorf("down.host expected timeout error, got %+v", results[2])
    }
}
