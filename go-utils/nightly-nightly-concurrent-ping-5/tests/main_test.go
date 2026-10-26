package main

import (
    "fmt"
    "testing"
    "time"
)

type MockPingProvider struct {
    delays map[string]time.Duration
    errs   map[string]error
}

func (m MockPingProvider) Ping(host string) (time.Duration, error) {
    if err, ok := m.errs[host]; ok {
        return 0, err
    }
    if d, ok := m.delays[host]; ok {
        return d, nil
    }
    return 0, nil
}

// TestPingHosts verifies that PingHosts correctly aggregates results,
// handling both successful pings and unreachable hosts.
func TestPingHosts(t *testing.T) {
    // Mock rationale: deterministic latencies for hosts
    mock := MockPingProvider{
        delays: map[string]time.Duration{
            "example.com": 100 * time.Millisecond,
            "localhost":   10 * time.Millisecond,
        },
        errs: map[string]error{
            "badhost": fmt.Errorf("unreachable"),
        },
    }
    hosts := []string{"example.com", "localhost", "badhost"}
    results := PingHosts(mock, hosts)
    if got := results["example.com"]; got != 100*time.Millisecond {
        t.Errorf("expected 100ms for example.com, got %v", got)
    }
    if got := results["localhost"]; got != 10*time.Millisecond {
        t.Errorf("expected 10ms for localhost, got %v", got)
    }
    if got := results["badhost"]; got != -1 {
        t.Errorf("expected -1 for badhost (unreachable), got %v", got)
    }
}
