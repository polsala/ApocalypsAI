package main

import (
    "errors"
    "net"
    "testing"
    "time"
)

// mockConn implements net.Conn but does nothing; used for successful mock.
type mockConn struct{}
func (m mockConn) Read(b []byte) (int, error)               { return 0, nil }
func (m mockConn) Write(b []byte) (int, error)              { return len(b), nil }
func (m mockConn) Close() error                             { return nil }
func (m mockConn) LocalAddr() net.Addr                      { return nil }
func (m mockConn) RemoteAddr() net.Addr                     { return nil }
func (m mockConn) SetDeadline(t time.Time) error            { return nil }
func (m mockConn) SetReadDeadline(t time.Time) error        { return nil }
func (m mockConn) SetWriteDeadline(t time.Time) error       { return nil }

func TestPingHostSuccess(t *testing.T) {
    // Save original and restore after test.
    orig := dialContext
    defer func() { dialContext = orig }()

    // Mock that pretends a 10ms latency.
    dialContext = func(network, address string, timeout time.Duration) (net.Conn, error) {
        time.Sleep(10 * time.Millisecond) // # Mock rationale: simulate network delay.
        return mockConn{}, nil
    }

    res := pingHost("example.com", 1*time.Second)
    if !res.Reachable {
        t.Fatalf("expected reachable, got not reachable")
    }
    if res.LatencyMs < 9 || res.LatencyMs > 30 {
        t.Fatalf("unexpected latency %v ms", res.LatencyMs)
    }
    if res.Error != "" {
        t.Fatalf("unexpected error: %s", res.Error)
    }
}

func TestPingHostFailure(t *testing.T) {
    orig := dialContext
    defer func() { dialContext = orig }()

    dialContext = func(network, address string, timeout time.Duration) (net.Conn, error) {
        return nil, errors.New("mock connection refused") // # Mock rationale: simulate failure.
    }

    res := pingHost("nonexistent.local", 1*time.Second)
    if res.Reachable {
        t.Fatalf("expected not reachable")
    }
    if res.Error != "mock connection refused" {
        t.Fatalf("unexpected error message: %s", res.Error)
    }
}
