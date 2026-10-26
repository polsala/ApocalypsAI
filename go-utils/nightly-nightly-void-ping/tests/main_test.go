package main

import (
    "reflect"
    "testing"
)

func TestComputeLatency(t *testing.T) {
    // "example.com" -> sum of bytes = 1113, (1113 % 100) + 1 = 14
    got := computeLatency("example.com")
    want := 14
    if got != want {
        t.Fatalf("computeLatency('example.com') = %d; want %d", got, want)
    }
}

func TestPingHosts(t *testing.T) {
    hosts := []string{"example.com", "test"}
    // Expected latencies:
    // "example.com" -> 14 (see above)
    // "test" -> sum 448, (448 % 100) + 1 = 49
    want := []Result{{Host: "example.com", LatencyMs: 14}, {Host: "test", LatencyMs: 49}}
    got := pingHosts(hosts)
    if !reflect.DeepEqual(got, want) {
        t.Fatalf("pingHosts returned %v; want %v", got, want)
    }
}
