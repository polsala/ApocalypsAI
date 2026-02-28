package main

import (
    "errors"
    "fmt"
    "net"
    "testing"
    "time"
)

type mockConn struct{}

func (m mockConn) Read(b []byte) (int, error)   { return 0, nil }
func (m mockConn) Write(b []byte) (int, error)  { return len(b), nil }
func (m mockConn) Close() error                 { return nil }
func (m mockConn) LocalAddr() net.Addr          { return nil }
func (m mockConn) RemoteAddr() net.Addr         { return nil }
func (m mockConn) SetDeadline(t time.Time) error { return nil }
func (m mockConn) SetReadDeadline(t time.Time) error { return nil }
func (m mockConn) SetWriteDeadline(t time.Time) error { return nil }

func mockDial(openPorts map[int]bool) dialFunc {
    return func(network, address string) (net.Conn, error) {
        var port int
        _, err := fmt.Sscanf(address, "%*[^:]:%d", &port)
        if err != nil {
            return nil, err
        }
        if openPorts[port] {
            return mockConn{}, nil
        }
        return nil, errors.New("closed")
    }
}

func TestScanPort(t *testing.T) {
    open := map[int]bool{80: true}
    d := mockDial(open)

    if !scanPort("example.com", 80, d) {
        t.Errorf("expected port 80 to be open")
    }
    if scanPort("example.com", 81, d) {
        t.Errorf("expected port 81 to be closed")
    }
}

func TestScanPorts(t *testing.T) {
    open := map[int]bool{22: true, 80: true}
    d := mockDial(open)

    result := scanPorts("example.com", 20, 85, 5, d)
    if len(result) != 2 {
        t.Fatalf("expected 2 open ports, got %d", len(result))
    }
    found22, found80 := false, false
    for _, p := range result {
        if p == 22 {
            found22 = true
        }
        if p == 80 {
            found80 = true
        }
    }
    if !found22 || !found80 {
        t.Errorf("did not find expected open ports")
    }
}
