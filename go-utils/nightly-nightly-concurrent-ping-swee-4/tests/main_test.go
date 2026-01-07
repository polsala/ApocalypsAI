package main

import (
    "errors"
    "net"
    "testing"
    "time"
)

// MockConn implements net.Conn with minimal stub methods.
type MockConn struct{}

func (m MockConn) Read(b []byte) (int, error)   { return 0, nil }
func (m MockConn) Write(b []byte) (int, error)  { return len(b), nil }
func (m MockConn) Close() error                 { return nil }
func (m MockConn) LocalAddr() net.Addr          { return nil }
func (m MockConn) RemoteAddr() net.Addr         { return nil }
func (m MockConn) SetDeadline(t time.Time) error      { return nil }
func (m MockConn) SetReadDeadline(t time.Time) error  { return nil }
func (m MockConn) SetWriteDeadline(t time.Time) error { return nil }

func TestPingHosts_Mocked(t *testing.T) {
    // # Mock rationale: replace dialer with deterministic behavior for fast, slow, and down hosts.
    originalDialer := dialer
    defer func() { dialer = originalDialer }()

    dialer = func(network, address string, timeout time.Duration) (net.Conn, error) {
        switch address {
        case "fast.local:80":
            // Simulate ~10ms latency.
            time.Sleep(10 * time.Millisecond)
            return MockConn{}, nil
        case "slow.local:80":
            // Simulate ~200ms latency.
            time.Sleep(200 * time.Millisecond)
            return MockConn{}, nil
        case "down.local:80":
            return nil, errors.New("connection refused")
        default:
            return nil, errors.New("unknown host")
        }
    }

    hosts := []string{"fast.local:80", "slow.local:80", "down.local:80"}
    results := PingHosts(hosts, 1*time.Second, 3)

    if len(results) != 3 {
        t.Fatalf("expected 3 results, got %d", len(results))
    }

    for _, r := range results {
        switch r.Host {
        case "fast.local:80":
            if !r.Reachable || r.LatencyMs < 10 || r.LatencyMs > 30 {
                t.Errorf("fast host latency unexpected: %+v", r)
            }
        case "slow.local:80":
            if !r.Reachable || r.LatencyMs < 200 || r.LatencyMs > 250 {
                t.Errorf("slow host latency unexpected: %+v", r)
            }
        case "down.local:80":
            if r.Reachable {
                t.Errorf("down host should be unreachable: %+v", r)
            }
            if r.LatencyMs != 0 {
                t.Errorf("down host latency should be 0: %+v", r)
            }
        }
    }
}
