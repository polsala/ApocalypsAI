package main

import (
    "net"
    "testing"
    "time"
)

// startMockTCPServer launches a TCP listener on the given address (use "127.0.0.1:0" for an OS‑chosen port).
// It accepts connections and immediately closes them, simulating a fast‑responding service.
func startMockTCPServer(t *testing.T, address string) net.Listener {
    ln, err := net.Listen("tcp", address)
    if err != nil {
        t.Fatalf("failed to start mock server: %v", err)
    }
    go func() {
        for {
            conn, err := ln.Accept()
            if err != nil {
                return // listener closed
            }
            conn.Close()
        }
    }()
    return ln
}

func TestPingHostSuccess(t *testing.T) {
    // Mock rationale: start a local TCP server that accepts connections instantly.
    ln := startMockTCPServer(t, "127.0.0.1:0")
    defer ln.Close()
    host := ln.Addr().String()
    dur, err := PingHost(host, 1*time.Second)
    if err != nil {
        t.Fatalf("expected no error, got %v", err)
    }
    if dur <= 0 {
        t.Fatalf("expected positive duration, got %v", dur)
    }
}

func TestPingHostTimeout(t *testing.T) {
    // Mock rationale: attempt to connect to an address where nothing is listening.
    host := "127.0.0.1:9" // discard port, typically closed
    _, err := PingHost(host, 100*time.Millisecond)
    if err == nil {
        t.Fatalf("expected timeout error, got nil")
    }
}

func TestPingMultiple(t *testing.T) {
    // Mock rationale: two mock servers, one reachable, one not.
    ln1 := startMockTCPServer(t, "127.0.0.1:0")
    defer ln1.Close()
    reachable := ln1.Addr().String()
    unreachable := "127.0.0.1:9"

    hosts := []string{reachable, unreachable}
    results := PingMultiple(hosts, 500*time.Millisecond)

    if d, ok := results[reachable]; !ok || d <= 0 {
        t.Fatalf("expected positive duration for reachable host, got %v", d)
    }
    if d, ok := results[unreachable]; !ok || d >= 0 {
        t.Fatalf("expected negative duration for unreachable host, got %v", d)
    }
}
