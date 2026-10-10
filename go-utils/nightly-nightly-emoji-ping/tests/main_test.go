package main

import (
    "errors"
    "testing"
    "time"
)

// Mock rationale: replace the real network ping with deterministic responses.
func TestEmojiForLatency(t *testing.T) {
    cases := []struct {
        latency time.Duration
        expect  string
    }{
        {10 * time.Millisecond, "🚀"},
        {100 * time.Millisecond, "⚡"},
        {300 * time.Millisecond, "🐢"},
    }
    for _, c := range cases {
        got := emojiForLatency(c.latency)
        if got != c.expect {
            t.Fatalf("emojiForLatency(%v) = %s; want %s", c.latency, got, c.expect)
        }
    }
}

func TestFormatResult(t *testing.T) {
    // Success case
    line := formatResult("example.com", 42*time.Millisecond, nil)
    if line != "example.com: up (42ms) 🚀" {
        t.Fatalf("unexpected format: %s", line)
    }
    // Failure case
    line = formatResult("bad.host", 0, errors.New("timeout"))
    if line != "bad.host: down ❌" {
        t.Fatalf("unexpected format for error: %s", line)
    }
}

func TestRunPingsWithMock(t *testing.T) {
    // Save original pingFunc and restore after test.
    original := pingFunc
    defer func() { pingFunc = original }()

    // Mock rationale: provide deterministic latencies for given hosts.
    pingFunc = func(host string, timeout time.Duration) (time.Duration, error) {
        switch host {
        case "fast.host":
            return 30 * time.Millisecond, nil
        case "slow.host":
            return 200 * time.Millisecond, nil
        case "down.host":
            return 0, errors.New("unreachable")
        default:
            return 0, errors.New("unknown host")
        }
    }

    hosts := []string{"fast.host", "slow.host", "down.host"}
    results := runPings(hosts, 1*time.Second)
    expected := []string{
        "fast.host: up (30ms) 🚀",
        "slow.host: up (200ms) 🐢",
        "down.host: down ❌",
    }
    for i, exp := range expected {
        if results[i] != exp {
            t.Fatalf("result %d = %s; want %s", i, results[i], exp)
        }
    }
}
