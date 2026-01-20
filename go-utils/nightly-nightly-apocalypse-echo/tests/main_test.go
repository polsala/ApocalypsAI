package main

import (
    "math/rand"
    "net"
    "strings"
    "testing"
    "time"
)

// TestEchoServerClient starts an in‑process server and verifies that the client receives a correctly prefixed echo.
func TestEchoServerClient(t *testing.T) {
    // Use a fixed seed so the prefix is deterministic.
    rand.Seed(42)

    // Listen on an OS‑assigned port.
    l, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("failed to listen: %v", err)
    }
    defer l.Close()

    // Start server in background.
    go func() {
        // startServer will run until the listener is closed.
        if err := startServer(l); err != nil && !strings.Contains(err.Error(), "use of closed network connection") {
            t.Errorf("server error: %v", err)
        }
    }()

    // Give the server a moment to start.
    time.Sleep(10 * time.Millisecond)

    address := l.Addr().String()
    testMsg := "test-message"
    resp, err := clientSend(address, testMsg)
    if err != nil {
        t.Fatalf("clientSend failed: %v", err)
    }

    // Expected format: PREFIX: test-message
    parts := strings.SplitN(resp, ": ", 2)
    if len(parts) != 2 {
        t.Fatalf("unexpected response format: %s", resp)
    }
    prefix, payload := parts[0], parts[1]

    // Verify payload matches the original message.
    if payload != testMsg {
        t.Fatalf("payload mismatch: got %s, want %s", payload, testMsg)
    }

    // Verify prefix is one of the allowed values.
    allowed := map[string]bool{"WASTELAND": true, "RUINS": true, "SANDSTORM": true, "MUTANT": true, "RADIOACTIVE": true}
    if !allowed[prefix] {
        t.Fatalf("unexpected prefix: %s", prefix)
    }
}
