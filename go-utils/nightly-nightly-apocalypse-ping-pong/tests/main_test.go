package main

import (
    "net"
    "testing"
    "time"
)

// startMockServer starts a TCP listener that accepts connections immediately.
func startMockServer(t *testing.T) (addr string, closeFn func()) {
    ln, err := net.Listen("tcp", "127.0.0.1:0")
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
    return ln.Addr().String(), func() { ln.Close() }
}

// startSlowMockServer accepts connections after a delay.
func startSlowMockServer(t *testing.T, delay time.Duration) (addr string, closeFn func()) {
    ln, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("failed to start slow mock server: %v", err)
    }
    go func() {
        for {
            conn, err := ln.Accept()
            if err != nil {
                return
            }
            time.Sleep(delay)
            conn.Close()
        }
    }()
    return ln.Addr().String(), func() { ln.Close() }
}

func TestPingHostFast(t *testing.T) {
    addr, closeFn := startMockServer(t)
    defer closeFn()
    res := pingHost(addr, 2*time.Second)
    if res.Err != nil {
        t.Fatalf("expected no error, got %v", res.Err)
    }
    if res.Latency <= 0 {
        t.Fatalf("expected positive latency, got %v", res.Latency)
    }
    if rating(res.Latency) != "🐇 Rabbit speed" && rating(res.Latency) != "🐢 Turtle pace" {
        t.Fatalf("unexpected rating for fast host: %s", rating(res.Latency))
    }
}

func TestPingHostSlow(t *testing.T) {
    // Delay of 200ms should push latency into the "Sloth" category.
    addr, closeFn := startSlowMockServer(t, 200*time.Millisecond)
    defer closeFn()
    res := pingHost(addr, 2*time.Second)
    if res.Err != nil {
        t.Fatalf("expected no error, got %v", res.Err)
    }
    if rating(res.Latency) != "🦥 Sloth crawl" {
        t.Fatalf("expected sloth rating, got %s (latency %v)", rating(res.Latency), res.Latency)
    }
}

func TestPingHostUnreachable(t *testing.T) {
    // Use an address that is unlikely to be listening.
    res := pingHost("127.0.0.1:9", 500*time.Millisecond)
    if res.Err == nil {
        t.Fatalf("expected error for unreachable host")
    }
    if rating(res.Latency) != "❌ Unreachable" {
        t.Fatalf("expected unreachable rating, got %s", rating(res.Latency))
    }
}
