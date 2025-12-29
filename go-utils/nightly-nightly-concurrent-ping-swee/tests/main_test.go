package main

import (
    "bytes"
    "fmt"
    "os"
    "strings"
    "testing"
    "time"
)

func TestAverageLatency(t *testing.T) {
    // Mock pingFunc to return deterministic latencies.
    pingFunc = func(host string) (time.Duration, error) {
        switch host {
        case "fast.host":
            return 100 * time.Millisecond, nil
        case "slow.host":
            return 200 * time.Millisecond, nil
        default:
            return 0, fmt.Errorf("unknown host")
        }
    }
    defer func() { pingFunc = defaultPing }()

    // Capture stdout.
    var out bytes.Buffer
    r, w, _ := os.Pipe()
    oldStdout := os.Stdout
    os.Stdout = w

    // Prepare arguments and run main.
    os.Args = []string{"cmd", "fast.host", "slow.host"}
    go func() {
        main()
        w.Close()
    }()
    out.ReadFrom(r)
    os.Stdout = oldStdout

    got := strings.TrimSpace(out.String())
    expected := "Average latency: 150ms"
    if got != expected {
        t.Fatalf("expected %q, got %q", expected, got)
    }
}
