package main

import (
    "reflect"
    "testing"
    "time"
)

func TestAggregateAndFormatting(t *testing.T) {
    // Mock measureLatency to return deterministic values.
    original := measureLatency
    defer func() { measureLatency = original }()

    mockLatencies := map[string]time.Duration{
        "a.com": 30 * time.Millisecond,
        "b.com": 70 * time.Millisecond,
        "c.com": 0, // will simulate error
    }
    measureLatency = func(host string) (time.Duration, error) {
        if lat, ok := mockLatencies[host]; ok {
            if lat == 0 {
                return 0, fmt.Errorf("mock error")
            }
            return lat, nil
        }
        return 0, fmt.Errorf("unknown host")
    }

    hosts := []string{"b.com", "a.com", "c.com"}
    results := aggregate(hosts)

    // Expect sorting by latency, error last.
    expectedOrder := []string{"a.com", "b.com", "c.com"}
    gotOrder := []string{results[0].host, results[1].host, results[2].host}
    if !reflect.DeepEqual(expectedOrder, gotOrder) {
        t.Fatalf("unexpected order: got %v want %v", gotOrder, expectedOrder)
    }

    // Test formatting of successful results.
    formattedA := formatResult(results[0])
    if formattedA != "a.com   30ms  ███" {
        t.Fatalf("unexpected format for a.com: %s", formattedA)
    }
    formattedB := formatResult(results[1])
    if formattedB != "b.com   70ms  ███████" {
        t.Fatalf("unexpected format for b.com: %s", formattedB)
    }
    // Test error formatting.
    if !strings.Contains(formatResult(results[2]), "error") {
        t.Fatalf("expected error formatting for c.com, got %s", formatResult(results[2]))
    }
}
