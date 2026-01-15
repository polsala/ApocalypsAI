package main

import (
    "strings"
    "testing"
    "time"
)

func TestEchoServerClient(t *testing.T) {
    port := "9090"
    // Start the server in a separate goroutine.
    go func() {
        // In test we ignore the error because the server runs indefinitely.
        _ = startServer(port)
    }()
    // Give the server a moment to start listening.
    time.Sleep(100 * time.Millisecond)

    msg := "Hello apocalypse"
    resp, err := runClient(port, msg)
    if err != nil {
        t.Fatalf("client error: %v", err)
    }
    expected := "⚡️[Apocalypse] " + msg + "\n"
    if strings.TrimSpace(resp) != strings.TrimSpace(expected) {
        t.Fatalf("expected %q, got %q", expected, resp)
    }
}
