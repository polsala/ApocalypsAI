package main

import (
    "errors"
    "net"
    "testing"
    "time"
)

// mockDialSuccess always returns a successful connection.
func mockDialSuccess(network, address string, timeout time.Duration) (net.Conn, error) {
    // Return a dummy net.Conn implementation.
    return &mockConn{}, nil
}

// mockDialFailure always returns an error.
func mockDialFailure(network, address string, timeout time.Duration) (net.Conn, error) {
    return nil, errors.New("mock connection failure")
}

type mockConn struct{}

func (m *mockConn) Read(b []byte) (n int, err error)   { return 0, nil }
func (m *mockConn) Write(b []byte) (n int, err error)  { return len(b), nil }
func (m *mockConn) Close() error                       { return nil }
func (m *mockConn) LocalAddr() net.Addr                { return nil }
func (m *mockConn) RemoteAddr() net.Addr               { return nil }
func (m *mockConn) SetDeadline(t time.Time) error     { return nil }
func (m *mockConn) SetReadDeadline(t time.Time) error { return nil }
func (m *mockConn) SetWriteDeadline(t time.Time) error { return nil }

func TestPingHostWithDialSuccess(t *testing.T) {
    reachable, err := pingHostWithDial("example.com", 1*time.Second, mockDialSuccess)
    if err != nil {
        t.Fatalf("expected no error, got %v", err)
    }
    if !reachable {
        t.Fatalf("expected reachable == true")
    }
}

func TestPingHostWithDialFailure(t *testing.T) {
    reachable, err := pingHostWithDial("example.com", 1*time.Second, mockDialFailure)
    if err == nil {
        t.Fatalf("expected an error, got nil")
    }
    if reachable {
        t.Fatalf("expected reachable == false")
    }
}

func TestRateSurvival(t *testing.T) {
    tests := []struct {
        successes int
        total     int
        wantPct   int
        wantRate  string
    }{
        {4, 4, 100, "Radiation‑Free"},
        {3, 4, 75, "Well‑Equipped"},
        {2, 4, 50, "Barely Breathing"},
        {1, 4, 25, "Critical"},
        {0, 4, 0, "Doomsday Imminent"},
    }
    for _, tt := range tests {
        pct, rating := rateSurvival(tt.successes, tt.total)
        if pct != tt.wantPct || rating != tt.wantRate {
            t.Errorf("rateSurvival(%d,%d) = (%d, %s); want (%d, %s)", tt.successes, tt.total, pct, rating, tt.wantPct, tt.wantRate)
        }
    }
}
