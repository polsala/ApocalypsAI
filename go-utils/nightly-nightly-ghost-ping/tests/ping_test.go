package ping

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

// TestPingSuccess simulates a successful connection with a 50ms latency.
func TestPingSuccess(t *testing.T) {
    original := dialContext
    defer func() { dialContext = original }()
    dialContext = func(network, address string, timeout time.Duration) (net.Conn, error) {
        time.Sleep(50 * time.Millisecond) // simulate latency
        return mockConn{}, nil
    }

    dur, err := Ping("example.com", 1*time.Second)
    if err != nil {
        t.Fatalf("expected no error, got %v", err)
    }
    if dur < 50*time.Millisecond {
        t.Fatalf("expected at least 50ms latency, got %v", dur)
    }
}

// TestPingTimeout simulates a timeout scenario.
func TestPingTimeout(t *testing.T) {
    original := dialContext
    defer func() { dialContext = original }()
    dialContext = func(network, address string, timeout time.Duration) (net.Conn, error) {
        time.Sleep(timeout + 10*time.Millisecond) // exceed timeout
        return nil, errors.New("i/o timeout")
    }

    _, err := Ping("slowhost", 100*time.Millisecond)
    if err == nil {
        t.Fatalf("expected timeout error, got nil")
    }
}
