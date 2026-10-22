package main

import (
    "context"
    "net"
    "testing"
    "time"
)

func TestPingPongRoundTrip(t *testing.T) {
    // Start server on a random available port
    laddr := net.UDPAddr{IP: net.ParseIP("127.0.0.1"), Port: 0}
    conn, err := net.ListenUDP("udp", &laddr)
    if err != nil {
        t.Fatalf("failed to listen udp: %v", err)
    }
    defer conn.Close()
    port := conn.LocalAddr().(*net.UDPAddr).Port
    // Close the temporary listener; the server will bind to the same port.
    conn.Close()

    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    go func() {
        if err := runServer(ctx, port); err != nil {
            t.Errorf("server error: %v", err)
        }
    }()
    // Give the server a moment to start (deterministic small sleep)
    time.Sleep(10 * time.Millisecond)

    testMsg := "test‑payload"
    resp, dur, err := ping(net.JoinHostPort("127.0.0.1", fmt.Sprintf("%d", port)), testMsg)
    if err != nil {
        t.Fatalf("ping failed: %v", err)
    }
    if resp != testMsg {
        t.Fatalf("expected echo %q, got %q", testMsg, resp)
    }
    if dur <= 0 {
        t.Fatalf("expected positive round‑trip time, got %v", dur)
    }
}
