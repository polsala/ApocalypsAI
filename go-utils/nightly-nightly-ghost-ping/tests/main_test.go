package main

import (
    "errors"
    "net"
    "testing"
    "time"
)

// mockConn implements net.Conn but does nothing; used for successful mock connections.
type mockConn struct{ net.Conn }

func (m mockConn) Close() error { return nil }

// pingWithDialer is a test‑visible wrapper that allows injection of a custom dialer.
func pingWithDialer(host string, timeout time.Duration, dialer func(network, address string, timeout time.Duration) (net.Conn, error)) (time.Duration, error) {
    start := time.Now()
    conn, err := dialer("tcp", net.JoinHostPort(host, "80"), timeout)
    if err != nil {
        return 0, err
    }
    _ = conn.Close()
    return time.Since(start), nil
}

func TestPingWithDialer_Fast(t *testing.T) {
    // Simulate a 50ms successful connection.
    dialer := func(network, address string, timeout time.Duration) (net.Conn, error) {
        time.Sleep(50 * time.Millisecond)
        return mockConn{}, nil
    }
    lat, err := pingWithDialer("fast.example", 1*time.Second, dialer)
    if err != nil {
        t.Fatalf("expected no error, got %v", err)
    }
    if lat < 45*time.Millisecond || lat > 70*time.Millisecond {
        t.Fatalf("expected latency around 50ms, got %v", lat)
    }
}

func TestPingWithDialer_Slow(t *testing.T) {
    // Simulate a 250ms successful connection.
    dialer := func(network, address string, timeout time.Duration) (net.Conn, error) {
        time.Sleep(250 * time.Millisecond)
        return mockConn{}, nil
    }
    lat, err := pingWithDialer("slow.example", 1*time.Second, dialer)
    if err != nil {
        t.Fatalf("expected no error, got %v", err)
    }
    if lat < 240*time.Millisecond || lat > 300*time.Millisecond {
        t.Fatalf("expected latency around 250ms, got %v", lat)
    }
}

func TestPingWithDialer_Unreachable(t *testing.T) {
    // Simulate a connection error.
    dialer := func(network, address string, timeout time.Duration) (net.Conn, error) {
        return nil, errors.New("dial timeout")
    }
    _, err := pingWithDialer("dead.example", 100*time.Millisecond, dialer)
    if err == nil {
        t.Fatalf("expected an error, got nil")
    }
}
