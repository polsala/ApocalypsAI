package main

import (
    "fmt"
    "testing"
)

func mockProviderFactory(latencies map[string]int) LatencyProvider {
    return func(host string) (int, error) {
        if v, ok := latencies[host]; ok {
            return v, nil
        }
        return 0, fmt.Errorf("unknown host")
    }
}

func TestPingHosts(t *testing.T) {
    hosts := []string{"alpha", "beta", "gamma"}
    mockLat := map[string]int{
        "alpha": 10,
        "beta":  20,
        "gamma": 30,
    }
    provider := mockProviderFactory(mockLat)
    results := PingHosts(hosts, provider)
    for _, h := range hosts {
        if results[h] != mockLat[h] {
            t.Fatalf("expected %d for %s, got %d", mockLat[h], h, results[h])
        }
    }
}
