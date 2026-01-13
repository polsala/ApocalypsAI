package main

import (
    "errors"
    "net"
    "testing"
    "time"
)

// mockConn implements net.Conn but does nothing.
type mockConn struct{}
func (m *mockConn) Read(b []byte) (n int, err error)         { return 0, nil }
func (m *mockConn) Write(b []byte) (n int, err error)        { return len(b), nil }
func (m *mockConn) Close() error                           { return nil }
func (m *mockConn) LocalAddr() net.Addr                    { return nil }
func (m *mockConn) RemoteAddr() net.Addr                   { return nil }
func (m *mockConn) SetDeadline(t time.Time) error          { return nil }
func (m *mockConn) SetReadDeadline(t time.Time) error      { return nil }
func (m *mockConn) SetWriteDeadline(t time.Time) error     { return nil }

// mockDialTimeout simulates net.DialTimeout with predefined latencies.
func mockDialTimeout(network, address string, timeout time.Duration) (net.Conn, error) {
    // Mock rationale: return a connection after a fixed fake latency based on address.
    switch address {
    case "fast.example.com:80":
        // simulate 10ms latency
        time.Sleep(10 * time.Millisecond)
        return &mockConn{}, nil
    case "slow.example.com:80":
        // simulate 200ms latency
        time.Sleep(200 * time.Millisecond)
        return &mockConn{}, nil
    case "down.example.com:80":
        // simulate failure
        return nil, errors.New("connection refused")
    default:
        // default 50ms
        time.Sleep(50 * time.Millisecond)
        return &mockConn{}, nil
    }
}

func TestPingHosts(t *testing.T) {
    // Replace the real pingHost with a version that uses mockDialTimeout.
    originalPingHost := pingHost
    defer func() { pingHost = originalPingHost }()
    pingHost = func(address string, timeout time.Duration) (time.Duration, error) {
        start := time.Now()
        _, err := mockDialTimeout("tcp", address, timeout)
        return time.Since(start), err
    }

    hosts := []string{"fast.example.com", "slow.example.com", "down.example.com"}
    results := PingHosts(hosts, 1*time.Second)

    if r, ok := results["fast.example.com"]; !ok || r.err != nil {
        t.Fatalf("fast host should succeed, got err=%v", r.err)
    } else if r.latency > 30*time.Millisecond {
        t.Fatalf("fast host latency too high: %v", r.latency)
    }

    if r, ok := results["slow.example.com"]; !ok || r.err != nil {
        t.Fatalf("slow host should succeed, got err=%v", r.err)
    } else if r.latency < 150*time.Millisecond {
        t.Fatalf("slow host latency too low: %v", r.latency)
    }

    if r, ok := results["down.example.com"]; !ok || r.err == nil {
        t.Fatalf("down host should fail, err=%v", r.err)
    }
}

