package main

import (
    "errors"
    "testing"
    "time"
)

// mockPingHost replaces the real pingHost during tests.
func mockPingHost(host string, timeout time.Duration) (time.Duration, error) {
    // Simulate deterministic latencies based on host name.
    switch host {
    case "fast.example":
        return 10 * time.Millisecond, nil
    case "slow.example":
        return 1500 * time.Millisecond, nil
    case "dead.example":
        return 0, errors.New("timeout")
    default:
        return 0, errors.New("unknown host")
    }
}

func TestPingAll_Mocked(t *testing.T) {
    // Swap out the network function.
    originalDial := dialFunc
    defer func() { dialFunc = originalDial }()
    // Replace dialFunc with a stub that always succeeds instantly.
    dialFunc = func(network, address string, timeout time.Duration) (net.Conn, error) {
        // Extract host part before ':'
        hostPort := strings.Split(address, ":")
        host := hostPort[0]
        // Use mockPingHost to decide outcome.
        latency, err := mockPingHost(host, timeout)
        if err != nil {
            return nil, err
        }
        // Return a dummy net.Conn that pretends the connection lasted `latency`.
        // We don't need a real connection; just satisfy the interface.
        return &dummyConn{latency: latency}, nil
    }

    hosts := []string{"fast.example", "slow.example", "dead.example"}
    results := pingAll(hosts, 2*time.Second, 2)

    if len(results) != 3 {
        t.Fatalf("expected 3 results, got %d", len(results))
    }
    // Verify each result matches the mock expectations.
    for _, r := range results {
        switch r.Host {
        case "fast.example":
            if r.Err != nil || r.Latency != 10*time.Millisecond {
                t.Errorf("fast.example expected 10ms, got %v, err=%v", r.Latency, r.Err)
            }
        case "slow.example":
            if r.Err != nil || r.Latency != 1500*time.Millisecond {
                t.Errorf("slow.example expected 1500ms, got %v, err=%v", r.Latency, r.Err)
            }
        case "dead.example":
            if r.Err == nil {
                t.Errorf("dead.example expected error, got none")
            }
        default:
            t.Errorf("unexpected host %s", r.Host)
        }
    }
}

// dummyConn implements net.Conn but does nothing; it's only needed to satisfy the interface.
type dummyConn struct {
    latency time.Duration
}

func (d *dummyConn) Read(b []byte) (n int, err error)   { return 0, nil }
func (d *dummyConn) Write(b []byte) (n int, err error)  { return len(b), nil }
func (d *dummyConn) Close() error                       { return nil }
func (d *dummyConn) LocalAddr() net.Addr                { return nil }
func (d *dummyConn) RemoteAddr() net.Addr               { return nil }
func (d *dummyConn) SetDeadline(t time.Time) error     { return nil }
func (d *dummyConn) SetReadDeadline(t time.Time) error { return nil }
func (d *dummyConn) SetWriteDeadline(t time.Time) error { return nil }
