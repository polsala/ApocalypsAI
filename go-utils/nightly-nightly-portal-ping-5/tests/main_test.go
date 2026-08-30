package main

import (
    "strings"
    "testing"
)

// TestSimulateLatencyDeterministic ensures that the same host always yields the same latency
// and that different hosts produce different latencies (high probability).
func TestSimulateLatencyDeterministic(t *testing.T) {
    h1 := simulateLatency("example.com")
    h2 := simulateLatency("example.com")
    if h1 != h2 {
        t.Fatalf("Latency not deterministic for identical host: %v vs %v", h1, h2)
    }
    h3 := simulateLatency("different.com")
    if h1 == h3 {
        t.Fatalf("Different hosts produced identical latency (%v); unlikely", h1)
    }
}

// TestPingHosts verifies that PingHosts returns exactly one result per input host
// and that each result string contains the corresponding host name.
func TestPingHosts(t *testing.T) {
    hosts := []string{"alpha", "beta", "gamma"}
    results := PingHosts(hosts)
    if len(results) != len(hosts) {
        t.Fatalf("Expected %d results, got %d", len(hosts), len(results))
    }
    for i, r := range results {
        if !strings.Contains(r, hosts[i]) {
            t.Fatalf("Result %d does not contain expected host %s: %s", i, hosts[i], r)
        }
    }
}
