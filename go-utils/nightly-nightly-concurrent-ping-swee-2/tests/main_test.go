package main

import (
    "errors"
    "net"
    "testing"
    "time"
)

// mockConn implements net.Conn but does nothing; it satisfies the interface for testing.
type mockConn struct{}

func (m *mockConn) Read(b []byte) (n int, err error)   { return 0, nil }
func (m *mockConn) Write(b []byte) (n int, err error)  { return len(b), nil }
func (m *mockConn) Close() error                     { return nil }
func (m *mockConn) LocalAddr() net.Addr              { return nil }
func (m *mockConn) RemoteAddr() net.Addr             { return nil }
func (m *mockConn) SetDeadline(t time.Time) error    { return nil }
func (m *mockConn) SetReadDeadline(t time.Time) error { return nil }
func (m *mockConn) SetWriteDeadline(t time.Time) error { return nil }

// mockDialer returns a mockConn instantly for hosts that contain "ok", otherwise returns an error.
type mockDialer struct{}

func (d *mockDialer) DialContext(_ context.Context, _, address string) (net.Conn, error) {
    if address == "ok:80" {
        return &mockConn{}, nil
    }
    return nil, errors.New("dial error")
}

func TestPingHostSuccess(t *testing.T) {
    d := &mockDialer{}
    dur, err := PingHost(d, "ok:80", 2*time.Second)
    if err != nil {
        t.Fatalf("expected no error, got %v", err)
    }
    // Since mockDialer returns instantly, duration should be very small.
    if dur > 10*time.Millisecond {
        t.Fatalf("expected nearâzero duration, got %v", dur)
    }
}

func TestPingHostFailure(t *testing.T) {
    d := &mockDialer{}
    _, err := PingHost(d, "bad:80", 2*time.Second)
    if err == nil {
        t.Fatalf("expected error for bad host, got nil")
    }
}

func TestPingHostsConcurrent(t *testing.T) {
    d := &mockDialer{}
    hosts := []string{"ok:80", "bad:80", "ok:80"}
    results := PingHosts(d, hosts, 2*time.Second)
    if len(results) != 3 {
        t.Fatalf("expected 3 results, got %d", len(results))
    }
    if results["ok:80"] == 0 {
        t.Fatalf("expected nonâzero latency for ok host")
    }
    if results["bad:80"] != 0 {
        t.Fatalf("expected zero latency for unreachable host")
    }
}

