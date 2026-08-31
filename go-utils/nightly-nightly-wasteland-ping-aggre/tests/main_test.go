package main

import (
    "net"
    "testing"
    "time"
)

func startMockServer(t *testing.T, delay time.Duration) (addr string, closeFn func()) {
    ln, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("failed to start mock server: %v", err)
    }
    go func() {
        for {
            conn, err := ln.Accept()
            if err != nil {
                return
            }
            // simulate processing delay
            time.Sleep(delay)
            conn.Close()
        }
    }()
    return ln.Addr().String(), func() { ln.Close() }
}

// Mock rationale: we use local TCP listeners with controlled delays to produce deterministic latencies.
func TestPingHostsOrdering(t *testing.T) {
    // Create three servers with different delays.
    addrFast, closeFast := startMockServer(t, 10*time.Millisecond)
    defer closeFast()
    addrMedium, closeMedium := startMockServer(t, 50*time.Millisecond)
    defer closeMedium()
    addrSlow, closeSlow := startMockServer(t, 100*time.Millisecond)
    defer closeSlow()

    hosts := []string{addrFast, addrSlow, addrMedium}
    results := PingHosts(hosts)

    // Expect ordering: fast, medium, slow (all successful)
    if len(results) != 3 {
        t.Fatalf("expected 3 results, got %d", len(results))
    }
    if results[0].Host != addrFast {
        t.Errorf("expected first host %s, got %s", addrFast, results[0].Host)
    }
    if results[1].Host != addrMedium {
        t.Errorf("expected second host %s, got %s", addrMedium, results[1].Host)
    }
    if results[2].Host != addrSlow {
        t.Errorf("expected third host %s, got %s", addrSlow, results[2].Host)
    }
}
