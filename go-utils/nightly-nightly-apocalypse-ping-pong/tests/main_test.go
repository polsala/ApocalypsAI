package main

import (
    "errors"
    "net"
    "testing"
    "time"
)

type mockConn struct{}

func (m *mockConn) Read(b []byte) (int, error)   { return 0, nil }
func (m *mockConn) Write(b []byte) (int, error)  { return len(b), nil }
func (m *mockConn) Close() error                 { return nil }
func (m *mockConn) LocalAddr() net.Addr          { return nil }
func (m *mockConn) RemoteAddr() net.Addr         { return nil }
func (m *mockConn) SetDeadline(t time.Time) error      { return nil }
func (m *mockConn) SetReadDeadline(t time.Time) error  { return nil }
func (m *mockConn) SetWriteDeadline(t time.Time) error { return nil }

func TestPingHost(t *testing.T) {
    // Save original dialer and restore after test
    originalDialer := dialer
    defer func() { dialer = originalDialer }()

    // Mock dialer behavior
    dialer = func(network, address string, timeout time.Duration) (net.Conn, error) {
        if address == "goodhost:80" {
            return &mockConn{}, nil
        }
        return nil, errors.New("connection refused")
    }

    alive, err := pingHost("goodhost")
    if err != nil || !alive {
        t.Fatalf("expected goodhost to be alive")
    }

    alive, err = pingHost("badhost")
    if err == nil || alive {
        t.Fatalf("expected badhost to be unreachable")
    }
}
