package main

import (
    "fmt"
    "testing"
    "time"
)

// mockDialerFactory creates a DialerFunc that returns predefined durations or errors.
func mockDialerFactory(durations map[string]time.Duration, errHosts map[string]error) DialerFunc {
    return func(host string, timeout time.Duration) (time.Duration, error) {
        if d, ok := durations[host]; ok {
            return d, nil
        }
        if e, ok := errHosts[host]; ok {
            return 0, e
        }
        return 0, fmt.Errorf("unknown host %s", host)
    }
}

func TestPingHosts(t *testing.T) {
    hosts := []string{"alpha", "beta", "gamma"}
    mockDurations := map[string]time.Duration{
        "alpha": 100 * time.Millisecond,
        "beta":  200 * time.Millisecond,
    }
    mockErrors := map[string]error{
        "gamma": fmt.Errorf("network unreachable"),
    }
    dialer := mockDialerFactory(mockDurations, mockErrors)
    results := PingHosts(hosts, 1*time.Second, dialer)

    if got := results["alpha"]; got != 100*time.Millisecond {
        t.Errorf("alpha latency = %v, want %v", got, 100*time.Millisecond)
    }
    if got := results["beta"]; got != 200*time.Millisecond {
        t.Errorf("beta latency = %v, want %v", got, 200*time.Millisecond)
    }
    if got := results["gamma"]; got != -1 {
        t.Errorf("gamma latency = %v, want -1 for error", got)
    }
}
