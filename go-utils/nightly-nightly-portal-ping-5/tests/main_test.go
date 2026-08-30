package main

import (
    "fmt"
    "net"
    "testing"
    "time"
)

// mockDial returns a dialFunc that pretends certain ports are open.
func mockDial(openPorts map[int]bool) dialFunc {
    return func(network, address string) (net.Conn, error) {
        var host string
        var port int
        // address format is "host:port"
        fmt.Sscanf(address, "%s:%d", &host, &port)
        if openPorts[port] {
            return &dummyConn{}, nil // simulate successful connection
        }
        return nil, fmt.Errorf("closed")
    }
}

// dummyConn satisfies net.Conn but does nothing.
type dummyConn struct{}

func (d *dummyConn) Read(b []byte) (int, error)               { return 0, nil }
func (d *dummyConn) Write(b []byte) (int, error)              { return len(b), nil }
func (d *dummyConn) Close() error                            { return nil }
func (d *dummyConn) LocalAddr() net.Addr                     { return nil }
func (d *dummyConn) RemoteAddr() net.Addr                    { return nil }
func (d *dummyConn) SetDeadline(t time.Time) error           { return nil }
func (d *dummyConn) SetReadDeadline(t time.Time) error       { return nil }
func (d *dummyConn) SetWriteDeadline(t time.Time) error      { return nil }

func TestScanPorts(t *testing.T) {
    // Define which ports the mock should consider open.
    open := map[int]bool{80: true, 443: true}
    dial := mockDial(open)

    portsToTest := []int{79, 80, 81, 442, 443, 444}
    var found []int
    for _, p := range portsToTest {
        if scanPort("example.com", p, time.Millisecond, dial) {
            found = append(found, p)
        }
    }

    expected := []int{80, 443}
    if len(found) != len(expected) {
        t.Fatalf("expected %v open ports, got %v", expected, found)
    }
    for i, v := range expected {
        if found[i] != v {
            t.Fatalf("expected port %d at index %d, got %d", v, i, found[i])
        }
    }
}
