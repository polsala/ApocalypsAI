package main

import (
    "errors"
    "testing"
    "time"
)

func TestPingAll(t *testing.T) {
    // Save original pingHost and restore after test.
    original := pingHost
    defer func() { pingHost = original }()

    // Mock implementation returning predetermined results.
    pingHost = func(host string, port int) (time.Duration, error) {
        switch host {
        case "fast.host":
            return 10 * time.Millisecond, nil
        case "slow.host":
            return 200 * time.Millisecond, nil
        default:
            return 0, errors.New("timeout")
        }
    }

    hosts := []string{"fast.host", "slow.host", "dead.host"}
    results := pingAll(hosts, 80)

    if len(results) != 3 {
        t.Fatalf("expected 3 results, got %d", len(results))
    }

    // Helper to find result by host.
    find := func(host string) *pingResult {
        for i := range results {
            if results[i].host == host {
                return &results[i]
            }
        }
        return nil
    }

    rFast := find("fast.host")
    if rFast == nil || rFast.err != nil || rFast.duration != 10*time.Millisecond {
        t.Errorf("unexpected result for fast.host: %+v", rFast)
    }

    rSlow := find("slow.host")
    if rSlow == nil || rSlow.err != nil || rSlow.duration != 200*time.Millisecond {
        t.Errorf("unexpected result for slow.host: %+v", rSlow)
    }

    rDead := find("dead.host")
    if rDead == nil || rDead.err == nil {
        t.Errorf("expected error for dead.host, got %+v", rDead)
    }
}
