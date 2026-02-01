package main

import (
    "net"
    "testing"
    "time"
)

// startTestServer starts a TCP listener on a random port and returns the address.
func startTestServer(t *testing.T) string {
    ln, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("failed to start test server: %v", err)
    }
    // Close the listener when the test finishes.
    t.Cleanup(func() { ln.Close() })
    // Accept connections in a separate goroutine to keep the server alive.
    go func() {
        for {
            conn, err := ln.Accept()
            if err != nil {
                return // Listener closed.
            }
            // Immediately close the connection; we only care about the handshake.
            conn.Close()
        }
    }()
    return ln.Addr().String()
}

func TestPingHostReachable(t *testing.T) {
    addr := startTestServer(t)
    timeout := 500 * time.Millisecond
    latency, err := PingHost(addr, timeout)
    if err != nil {
        t.Fatalf("expected reachable host, got error: %v", err)
    }
    if latency <= 0 {
        t.Fatalf("expected positive latency, got %d", latency)
    }
}

func TestPingHostUnreachable(t *testing.T) {
    // Choose an address that is unlikely to have a listener.
    // Using port 9 (discard) on localhost is typically closed.
    addr := "127.0.0.1:9"
    timeout := 200 * time.Millisecond
    _, err := PingHost(addr, timeout)
    if err == nil {
        t.Fatalf("expected error for unreachable host, got nil")
    }
}
