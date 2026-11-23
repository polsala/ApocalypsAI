package main

import (
    "context"
    "errors"
    "testing"
    "time"
)

// mockPing simulates latency based on host name.
func mockPing(ctx context.Context, host string, timeout time.Duration) (time.Duration, error) {
    switch host {
    case "fast.example":
        return 10 * time.Millisecond, nil
    case "slow.example":
        return 200 * time.Millisecond, nil
    case "fail.example":
        return 0, errors.New("connection refused")
    default:
        return 0, errors.New("unknown host")
    }
}

func TestPingHost_MixedResults(t *testing.T) {
    // Replace the global PingFunc with our mock.
    original := PingFunc
    PingFunc = mockPing
    defer func() { PingFunc = original }()

    ctx := context.Background()
    hosts := []string{"fast.example", "slow.example", "fail.example"}
    count := 2
    timeout := 1 * time.Second

    results := make([]PingResult, len(hosts))
    for i, h := range hosts {
        results[i] = pingHost(ctx, h, count, timeout)
    }

    // fast.example: two successful 10ms pings => avg 10ms
    if !results[0].Success || results[0].AvgLatencyMs != 10 {
        t.Errorf("fast.example expected success with 10ms avg, got %+v", results[0])
    }
    // slow.example: two successful 200ms pings => avg 200ms
    if !results[1].Success || results[1].AvgLatencyMs != 200 {
        t.Errorf("slow.example expected success with 200ms avg, got %+v", results[1])
    }
    // fail.example: all attempts fail => success false, avg 0
    if results[2].Success || results[2].AvgLatencyMs != 0 {
        t.Errorf("fail.example expected failure, got %+v", results[2])
    }
}
