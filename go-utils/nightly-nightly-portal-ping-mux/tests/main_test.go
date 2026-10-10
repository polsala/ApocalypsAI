package main

import (
    "net"
    "testing"
    "time"
)

// mockDialer returns a net.Conn that does nothing but satisfies the interface.
// It simulates an instantaneous successful connection.
func mockDialer(network, address string) (net.Conn, error) {
    // net.Pipe creates a pair of connected in‑memory connections.
    c1, c2 := net.Pipe()
    // Close the opposite end immediately; we only need a valid Conn.
    go func() { defer c2.Close(); select {} }()
    return c1, nil
}

func TestPingHostSuccess(t *testing.T) {
    addr := "example.com:80"
    res := pingHost(addr, mockDialer)
    if res.Err != nil {
        t.Fatalf("expected no error, got %v", res.Err)
    }
    // Since mockDialer is instantaneous, latency should be very small.
    if res.Latency > 5*time.Millisecond {
        t.Fatalf("expected latency < 5ms, got %v", res.Latency)
    }
}

func TestComputeStats(t *testing.T) {
    latencies := []time.Duration{10 * time.Millisecond, 20 * time.Millisecond, 30 * time.Millisecond}
    min, avg, max := computeStats(latencies)
    if min != 10*time.Millisecond {
        t.Errorf("expected min 10ms, got %v", min)
    }
    if avg != 20*time.Millisecond {
        t.Errorf("expected avg 20ms, got %v", avg)
    }
    if max != 30*time.Millisecond {
        t.Errorf("expected max 30ms, got %v", max)
    }
}
