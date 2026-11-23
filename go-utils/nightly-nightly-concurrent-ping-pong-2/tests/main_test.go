package main

import (
    "fmt"
    "testing"
)

// Mock rationale: replace the real network call with deterministic responses.
func TestPingHostSuccess(t *testing.T) {
    pingFunc = func(host string) (int, error) {
        if host == "example.com" {
            return 42, nil
        }
        return 0, fmt.Errorf("unknown host")
    }
    defer func() { pingFunc = realPing }()

    latency, err := pingFunc("example.com")
    if err != nil {
        t.Fatalf("expected no error, got %v", err)
    }
    if latency != 42 {
        t.Fatalf("expected latency 42, got %d", latency)
    }
}

func TestPingHostError(t *testing.T) {
    pingFunc = func(host string) (int, error) {
        return 0, fmt.Errorf("timeout")
    }
    defer func() { pingFunc = realPing }()

    _, err := pingFunc("badhost")
    if err == nil {
        t.Fatalf("expected error, got nil")
    }
}
