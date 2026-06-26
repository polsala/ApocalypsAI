package main

import (
    "errors"
    "net"
    "testing"
    "time"
)

type mockConn struct{}

func (m mockConn) Read(b []byte) (int, error)               { return 0, nil }
func (m mockConn) Write(b []byte) (int, error)              { return len(b), nil }
func (m mockConn) Close() error                             { return nil }
func (m mockConn) LocalAddr() net.Addr                      { return nil }
func (m mockConn) RemoteAddr() net.Addr                     { return nil }
func (m mockConn) SetDeadline(t time.Time) error           { return nil }
func (m mockConn) SetReadDeadline(t time.Time) error       { return nil }
func (m mockConn) SetWriteDeadline(t time.Time) error      { return nil }

// TestPingHostSuccess verifies that a successful connection is reported correctly.
func TestPingHostSuccess(t *testing.T) {
    originalDialer := dialer
    defer func() { dialer = originalDialer }()

    dialer = func(network, address string, timeout time.Duration) (net.Conn, error) {
        // Simulate 100ms latency.
        time.Sleep(100 * time.Millisecond)
        return mockConn{}, nil
    }

    r := pingHost("example.com", 1*time.Second)
    if !r.success {
        t.Fatalf("expected success, got failure")
    }
    if r.latency < 100*time.Millisecond {
        t.Fatalf("expected latency >= 100ms, got %v", r.latency)
    }
    if r.err != nil {
        t.Fatalf("expected no error, got %v", r.err)
    }
}

// TestPingHostFailure verifies that a failed connection is reported with an error.
func TestPingHostFailure(t *testing.T) {
    originalDialer := dialer
    defer func() { dialer = originalDialer }()

    dialer = func(network, address string, timeout time.Duration) (net.Conn, error) {
        // Simulate a quick failure.
        time.Sleep(50 * time.Millisecond)
        return nil, errors.New("mock connection refused")
    }

    r := pingHost("nonexistent.local", 1*time.Second)
    if r.success {
        t.Fatalf("expected failure, got success")
    }
    if r.err == nil {
        t.Fatalf("expected an error, got nil")
    }
    if r.latency < 50*time.Millisecond {
        t.Fatalf("expected latency >= 50ms, got %v", r.latency)
    }
}
