package main

import "testing"

func TestComputeLatency(t *testing.T) {
    // Helper to calculate expected latency using the same algorithm.
    expected := func(host string) int {
        sum := 0
        for _, r := range host {
            sum += int(r)
        }
        return (sum % 100) + 20
    }

    cases := []string{"example.com", "localhost", "8.8.8.8", "go.dev"}
    for _, host := range cases {
        got := computeLatency(host)
        want := expected(host)
        if got != want {
            t.Errorf("computeLatency(%s) = %d; want %d", host, got, want)
        }
    }
}

func TestPingHosts(t *testing.T) {
    hosts := []string{"alpha", "beta", "gamma"}
    results := pingHosts(hosts)
    if len(results) != len(hosts) {
        t.Fatalf("expected %d results, got %d", len(hosts), len(results))
    }
    for _, h := range hosts {
        if _, ok := results[h]; !ok {
            t.Errorf("missing result for host %s", h)
        }
    }
    // Verify that results are deterministic by recomputing.
    for _, h := range hosts {
        expected := computeLatency(h)
        if results[h] != expected {
            t.Errorf("result mismatch for %s: got %d, want %d", h, results[h], expected)
        }
    }
}
