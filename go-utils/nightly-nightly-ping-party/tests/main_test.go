package main

import (
    "net"
    "testing"
    "time"
)

func TestPingHostSuccess(t *testing.T) {
    // Mock rationale: start a local TCP server to guarantee a reachable host.
    ln, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("failed to start mock server: %v", err)
    }
    defer ln.Close()
    addr := ln.Addr().String()
    host, _, _ := net.SplitHostPort(addr)

    // Run PingHost against the mock server
    latency, err := PingHost(host, 1*time.Second)
    if err != nil {
        t.Fatalf("expected no error, got %v", err)
    }
    if latency <= 0 {
        t.Fatalf("expected positive latency, got %v", latency)
    }
}

func TestPingHostTimeout(t *testing.T) {
    // Mock rationale: use an unroutable IP to force a timeout.
    host := "10.255.255.1" // non‑routable address
    _, err := PingHost(host, 200*time.Millisecond)
    if err == nil {
        t.Fatalf("expected timeout error, got nil")
    }
}
