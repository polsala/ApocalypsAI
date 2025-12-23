package main

import (
    "fmt"
    "testing"
    "time"
)

func TestAggregate(t *testing.T) {
    // Mock PingFunc to avoid real network calls
    PingFunc = func(host string, timeout time.Duration) (time.Duration, error) {
        switch host {
        case "fast":
            return 50 * time.Millisecond, nil
        case "slow":
            return 200 * time.Millisecond, nil
        case "fail":
            return 0, fmt.Errorf("unreachable")
        default:
            return 100 * time.Millisecond, nil
        }
    }
    // Restore original after test
    defer func() { PingFunc = defaultPing }()

    hosts := []string{"fast", "slow", "fail"}
    min, avg, max, err := aggregate(hosts, 1*time.Second)
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if min != 50*time.Millisecond {
        t.Errorf("expected min 50ms, got %v", min)
    }
    if max != 200*time.Millisecond {
        t.Errorf("expected max 200ms, got %v", max)
    }
    expectedAvg := (50 + 200) * time.Millisecond / 2
    if avg != expectedAvg {
        t.Errorf("expected avg %v, got %v", expectedAvg, avg)
    }
}
