package main

import (
    "errors"
    "net"
    "testing"
    "time"
)

// mockConn implements net.Conn but does nothing; it satisfies the interface.
type mockConn struct{ net.Conn }

func (m mockConn) Close() error                       { return nil }
func (m mockConn) Read(b []byte) (int, error)        { return 0, nil }
func (m mockConn) Write(b []byte) (int, error)       { return len(b), nil }
func (m mockConn) LocalAddr() net.Addr                { return nil }
func (m mockConn) RemoteAddr() net.Addr               { return nil }
func (m mockConn) SetDeadline(t time.Time) error     { return nil }
func (m mockConn) SetReadDeadline(t time.Time) error { return nil }
func (m mockConn) SetWriteDeadline(t time.Time) error { return nil }

// mockDialer returns a connection after sleeping for the specified delay.
func mockDialer(delay time.Duration, shouldFail bool) func(network, address string, timeout time.Duration) (net.Conn, error) {
    return func(network, address string, timeout time.Duration) (net.Conn, error) {
        if shouldFail {
            return nil, errors.New("mock failure")
        }
        // Simulate network latency.
        time.Sleep(delay)
        return mockConn{}, nil
    }
}

func TestPingHostFast(t *testing.T) {
    latency, err := pingHost("fast.example", mockDialer(30*time.Millisecond, false))
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if latency < 30*time.Millisecond || latency > 40*time.Millisecond {
        t.Fatalf("expected latency around 30ms, got %v", latency)
    }
    emoji, desc := animalMetaphor(latency)
    if emoji != "🐆" || desc != "Cheetah (fast)" {
        t.Fatalf("unexpected metaphor: %s %s", emoji, desc)
    }
}

func TestPingHostModerate(t *testing.T) {
    latency, err := pingHost("moderate.example", mockDialer(120*time.Millisecond, false))
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    emoji, desc := animalMetaphor(latency)
    if emoji != "🐇" || desc != "Rabbit (moderate)" {
        t.Fatalf("unexpected metaphor: %s %s", emoji, desc)
    }
}

func TestPingHostSlow(t *testing.T) {
    latency, err := pingHost("slow.example", mockDialer(250*time.Millisecond, false))
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    emoji, desc := animalMetaphor(latency)
    if emoji != "🐢" || desc != "Turtle (slow)" {
        t.Fatalf("unexpected metaphor: %s %s", emoji, desc)
    }
}

func TestPingHostFailure(t *testing.T) {
    _, err := pingHost("fail.example", mockDialer(0, true))
    if err == nil {
        t.Fatalf("expected error but got nil")
    }
}
