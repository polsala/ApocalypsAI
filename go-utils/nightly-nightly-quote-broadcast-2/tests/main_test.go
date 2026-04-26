package main

import (
    "io"
    "net"
    "strings"
    "testing"
    "time"
)

// TestQuoteBroadcast verifies that a client receives the expected first quote
// from a freshly started server. The server uses a deterministic round‑robin
// counter, so the first connection should always get the first element of the
// quotes slice.
func TestQuoteBroadcast(t *testing.T) {
    // Start a listener on an OS‑assigned port.
    ln, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("failed to listen: %v", err)
    }
    defer ln.Close()

    // Run the server loop in a goroutine.
    go func() {
        for {
            conn, err := ln.Accept()
            if err != nil {
                // Listener closed, exit goroutine.
                return
            }
            go handleConn(conn)
        }
    }()

    // Give the server a moment to start.
    time.Sleep(10 * time.Millisecond)

    // Connect as a client.
    conn, err := net.Dial("tcp", ln.Addr().String())
    if err != nil {
        t.Fatalf("client failed to connect: %v", err)
    }
    defer conn.Close()

    // Read the quote.
    data, err := io.ReadAll(conn)
    if err != nil {
        t.Fatalf("failed to read from server: %v", err)
    }
    received := strings.TrimSpace(string(data))
    expected := quotes[0]
    if received != expected {
        t.Fatalf("expected %q, got %q", expected, received)
    }
}
