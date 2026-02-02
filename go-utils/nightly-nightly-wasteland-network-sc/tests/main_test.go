package main

import (
    "errors"
    "net"
    "strings"
    "testing"
)

// mockDial simulates open ports: 22 and 443 are open, others closed.
func mockDial(network, address string) (net.Conn, error) {
    if strings.HasSuffix(address, ":22") || strings.HasSuffix(address, ":443") {
        // Return a dummy net.Conn using net.Pipe()
        c1, c2 := net.Pipe()
        // Close the other end immediately; we only need a non‑nil Conn.
        c2.Close()
        return c1, nil
    }
    return nil, errors.New("connection refused")
}

func TestScanHost(t *testing.T) {
    host := "10.0.0.1"
    ports := []int{22, 80, 443}
    open := scanHost(host, ports, mockDial)
    expected := []int{22, 443}
    if len(open) != len(expected) {
        t.Fatalf("expected %d open ports, got %d", len(expected), len(open))
    }
    for i, v := range expected {
        if open[i] != v {
            t.Fatalf("expected port %d at index %d, got %d", v, i, open[i])
        }
    }
}
