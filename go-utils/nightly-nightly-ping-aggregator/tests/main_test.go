package main

import (
    "context"
    "errors"
    "net"
    "testing"
    "time"
)

type mockConn struct{}

func (m *mockConn) Read(b []byte) (int, error)         { return 0, nil }
func (m *mockConn) Write(b []byte) (int, error)        { return len(b), nil }
func (m *mockConn) Close() error                       { return nil }
func (m *mockConn) LocalAddr() net.Addr                { return nil }
func (m *mockConn) RemoteAddr() net.Addr               { return nil }
func (m *mockConn) SetDeadline(t time.Time) error     { return nil }
func (m *mockConn) SetReadDeadline(t time.Time) error { return nil }
func (m *mockConn) SetWriteDeadline(t time.Time) error { return nil }

type mockDialer struct {
    delays   map[string]time.Duration
    errAddrs map[string]bool
}

func (m *mockDialer) DialContext(ctx context.Context, network, address string) (net.Conn, error) {
    if m.errAddrs[address] {
        return nil, errors.New("mock connection error")
    }
    d := m.delays[address]
    select {
    case <-time.After(d):
        return &mockConn{}, nil
    case <-ctx.Done():
        return nil, ctx.Err()
    }
}

func TestPingAll(t *testing.T) {
    mock := &mockDialer{
        delays: map[string]time.Duration{
            "fast:80": 10 * time.Millisecond,
            "slow:80": 150 * time.Millisecond,
        },
        errAddrs: map[string]bool{
            "down:80": true,
        },
    }
    addrs := []string{"fast:80", "slow:80", "down:80"}
    timeout := 200 * time.Millisecond
    results := PingAll(mock, addrs, timeout)

    if dur, ok := results["fast:80"]; !ok || dur < 0 || dur > 20*time.Millisecond {
        t.Errorf("fast address latency unexpected: %v", dur)
    }
    if dur, ok := results["slow:80"]; !ok || dur < 140*time.Millisecond {
        t.Errorf("slow address latency unexpected: %v", dur)
    }
    if dur, ok := results["down:80"]; !ok || dur >= 0 {
        t.Errorf("down address should be unreachable, got: %v", dur)
    }
}
