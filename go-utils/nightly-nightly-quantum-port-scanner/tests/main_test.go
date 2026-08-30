package main

import (
    "errors"
    "net"
    "testing"
    "time"
)

type mockConn struct{}
func (m mockConn) Read(b []byte) (int, error) { return 0, nil }
func (m mockConn) Write(b []byte) (int, error) { return len(b), nil }
func (m mockConn) Close() error { return nil }
func (m mockConn) LocalAddr() net.Addr { return nil }
func (m mockConn) RemoteAddr() net.Addr { return nil }
func (m mockConn) SetDeadline(t time.Time) error { return nil }
func (m mockConn) SetReadDeadline(t time.Time) error { return nil }
func (m mockConn) SetWriteDeadline(t time.Time) error { return nil }

func mockDialer(openPorts map[string]bool) dialFunc {
    return func(network, address string) (net.Conn, error) {
        if openPorts[address] {
            return mockConn{}, nil }
        return nil, errors.New("closed")
    }
}

func TestScanPort(t *testing.T) {
    open := map[string]bool{
        "localhost:80": true,
        "localhost:22": false,
    }
    if !scanPort("localhost", "80", mockDialer(open)) {
        t.Errorf("expected port 80 to be open")
    }
    if scanPort("localhost", "22", mockDialer(open)) {
        t.Errorf("expected port 22 to be closed")
    }
}
