package main

import (
    "fmt"
    "reflect"
    "testing"
)

// Mock rationale: replace PingFunc with deterministic responses.
func TestPingAll_Mocked(t *testing.T) {
    original := PingFunc
    defer func() { PingFunc = original }()

    mockResponses := map[string]int{
        "example.com": 42,
        "8.8.8.8":     15,
        "bad.host":   -1,
    }

    PingFunc = func(host string) (int, error) {
        if latency, ok := mockResponses[host]; ok {
            if latency >= 0 {
                return latency, nil
            }
            return 0, fmt.Errorf("mock failure")
        }
        return 0, fmt.Errorf("unknown host")
    }

    hosts := []string{"example.com", "8.8.8.8", "bad.host"}
    got := PingAll(hosts)

    expected := map[string]int{
        "example.com": 42,
        "8.8.8.8":     15,
        "bad.host":   -1,
    }

    if !reflect.DeepEqual(got, expected) {
        t.Fatalf("expected %v, got %v", expected, got)
    }
}
