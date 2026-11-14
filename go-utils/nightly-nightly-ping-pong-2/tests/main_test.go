package main

import (
    "errors"
    "testing"
    "time"
)

func TestRunPings_Mocked(t *testing.T) {
    // Mock ping function: returns preset latencies or error.
    mock := func(host string) (time.Duration, error) {
        switch host {
        case "fast.com:80":
            return 30 * time.Millisecond, nil
        case "slow.com:80":
            return 200 * time.Millisecond, nil
        case "down.com:80":
            return 0, errors.New("timeout")
        default:
            return 0, errors.New("unknown")
        }
    }
    // Swap out the real ping.
    original := ping
    ping = mock
    defer func() { ping = original }()

    hosts := []string{"fast.com:80", "slow.com:80", "down.com:80"}
    results := runPings(hosts)

    if len(results) != 3 {
        t.Fatalf("expected 3 results, got %d", len(results))
    }

    // Verify each result matches the mock.
    for _, r := range results {
        switch r.Host {
        case "fast.com:80":
            if r.Err != nil || r.Latency != 30*time.Millisecond {
                t.Errorf("fast host unexpected: %+v", r)
            }
        case "slow.com:80":
            if r.Err != nil || r.Latency != 200*time.Millisecond {
                t.Errorf("slow host unexpected: %+v", r)
            }
        case "down.com:80":
            if r.Err == nil {
                t.Errorf("down host expected error")
            }
        }
    }
}
