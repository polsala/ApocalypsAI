package main

import (
    "errors"
    "net"
    "testing"
    "time"
)

// mockConn implements net.Conn with no‑op methods for testing.
type mockConn struct{}

func (m *mockConn) Read(b []byte) (n int, err error)   { return 0, nil }
func (m *mockConn) Write(b []byte) (n int, err error)  { return len(b), nil }
func (m *mockConn) Close() error                       { return nil }
func (m *mockConn) LocalAddr() net.Addr                { return nil }
func (m *mockConn) RemoteAddr() net.Addr               { return nil }
func (m *mockConn) SetDeadline(t time.Time) error     { return nil }
func (m *mockConn) SetReadDeadline(t time.Time) error { return nil }
func (m *mockConn) SetWriteDeadline(t time.Time) error { return nil }

// TestPingSuccess verifies that ping returns true when the mock dial succeeds.
func TestPingSuccess(t *testing.T) {
    original := dialTimeout
    defer func() { dialTimeout = original }()
    dialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
        return &mockConn{}, nil // simulate successful connection
    }

    if !ping("alive.example.com", 1*time.Second) {
        t.Fatalf("expected ping to succeed")
    }
}

// TestPingFailure verifies that ping returns false when the mock dial fails.
func TestPingFailure(t *testing.T) {
    original := dialTimeout
    defer func() { dialTimeout = original }()
    dialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
        return nil, errors.New("dial error") // simulate failure
    }

    if ping("dead.example.com", 1*time.Second) {
        t.Fatalf("expected ping to fail")
    }
}
