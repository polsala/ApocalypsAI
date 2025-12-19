package main

import (
    "errors"
    "io"
    "os"
    "strings"
    "testing"
    "time"
)

func TestLatencyRanking(t *testing.T) {
    // Mock latencyFunc to return deterministic results.
    original := latencyFunc
    defer func() { latencyFunc = original }()

    latencyFunc = func(host string, timeout time.Duration) (time.Duration, error) {
        switch host {
        case "fast.example.com:80":
            return 10 * time.Millisecond, nil
        case "slow.example.com:80":
            return 100 * time.Millisecond, nil
        case "down.example.com:80":
            return 0, errors.New("timeout")
        default:
            return 0, errors.New("unknown")
        }
    }

    // Simulate command line arguments.
    origArgs := os.Args
    defer func() { os.Args = origArgs }()
    os.Args = []string{"cmd", "fast.example.com:80", "slow.example.com:80", "down.example.com:80"}

    // Capture stdout.
    r, w, _ := os.Pipe()
    oldStdout := os.Stdout
    os.Stdout = w

    main()

    w.Close()
    os.Stdout = oldStdout
    var buf strings.Builder
    io.Copy(&buf, r)

    output := buf.String()
    expected := []string{
        "🏆 1️⃣ fast.example.com:80 – 10.0ms",
        "🥈 2️⃣ slow.example.com:80 – 100.0ms",
        "🥉 3️⃣ down.example.com:80 – timeout",
    }
    for _, line := range expected {
        if !strings.Contains(output, line) {
            t.Fatalf("expected line %q not found in output: %s", line, output)
        }
    }
}
