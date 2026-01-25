package main

import (
    "context"
    "errors"
    "net"
    "testing"
    "time"
)

type mockDialer struct {
    delays map[string]time.Duration
    errs   map[string]error
}

func (m *mockDialer) DialContext(ctx context.Context, network, address string) (net.Conn, error) {
    if err, ok := m.errs[address]; ok {
        return nil, err
    }
    if d, ok := m.delays[address]; ok {
        time.Sleep(d)
        return &mockConn{}, nil
    }
    // default immediate success
    return &mockConn{}, nil
}

type mockConn struct{}

func (c *mockConn) Read(b []byte) (n int, err error)   { return 0, nil }
func (c *mockConn) Write(b []byte) (n int, err error)  { return len(b), nil }
func (c *mockConn) Close() error                       { return nil }
func (c *mockConn) LocalAddr() net.Addr                { return nil }
func (c *mockConn) RemoteAddr() net.Addr               { return nil }
func (c *mockConn) SetDeadline(t time.Time) error     { return nil }
func (c *mockConn) SetReadDeadline(t time.Time) error { return nil }
func (c *mockConn) SetWriteDeadline(t time.Time) error { return nil }

func TestPingHost_Mocked(t *testing.T) {
    md := &mockDialer{
        delays: map[string]time.Duration{
            "fast:80": 10 * time.Millisecond,
            "slow:80": 200 * time.Millisecond,
        },
        errs: map[string]error{
            "fail:80": errors.New("dial error"),
        },
    }

    tests := []struct {
        addr     string
        wantOpen bool
        wantLat  time.Duration
    }{
        {"fast:80", true, 10 * time.Millisecond},
        {"slow:80", true, 200 * time.Millisecond},
        {"fail:80", false, 0},
    }

    for _, tt := range tests {
        res := pingHost(md, tt.addr)
        if res.Open != tt.wantOpen {
            t.Errorf("pingHost(%s) open=%v, want %v", tt.addr, res.Open, tt.wantOpen)
        }
        if tt.wantOpen && res.Latency < tt.wantLat {
            t.Errorf("pingHost(%s) latency=%v, want at least %v", tt.addr, res.Latency, tt.wantLat)
        }
    }
}
