package main

import (
    "errors"
    "testing"
    "time"
)

func TestRun_MixedResults(t *testing.T) {
    // Save original PingFunc and restore after test.
    original := PingFunc
    defer func() { PingFunc = original }()

    // Mock implementation returning predetermined outcomes.
    PingFunc = func(address string) (time.Duration, error) {
        switch address {
        case "good:80":
            return 50 * time.Millisecond, nil
        case "bad:81":
            return 0, errors.New("connection refused")
        default:
            return 0, errors.New("unknown host")
        }
    }

    addrs := []string{"good:80", "bad:81", "mystery:99"}
    results := run(addrs)

    if len(results) != 3 {
        t.Fatalf("expected 3 results, got %d", len(results))
    }

    // good host should be successful.
    if !results[0].Success || results[0].Latency != 50*time.Millisecond {
        t.Errorf("expected good success, got %+v", results[0])
    }
    // bad host should fail with specific error.
    if results[1].Success || results[1].Err != "connection refused" {
        t.Errorf("expected bad failure, got %+v", results[1])
    }
    // unknown host should also fail.
    if results[2].Success || results[2].Err != "unknown host" {
        t.Errorf("expected unknown failure, got %+v", results[2])
    }
}
