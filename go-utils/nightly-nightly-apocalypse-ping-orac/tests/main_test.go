package main

import (
    "reflect"
    "testing"
)

// mockProvider returns deterministic latency based on host length.
func mockProvider(host string) (int, error) {
    return len(host) * 10, nil
}

func TestPingHostsDeterministic(t *testing.T) {
    hosts := []string{"a", "bb", "ccc"}
    expected := map[string]int{
        "a":   10,
        "bb":  20,
        "ccc": 30,
    }
    got := PingHosts(hosts, mockProvider)
    if !reflect.DeepEqual(got, expected) {
        t.Fatalf("expected %v, got %v", expected, got)
    }
}
