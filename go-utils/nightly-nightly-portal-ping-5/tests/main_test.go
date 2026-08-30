package main

import (
    "errors"
    "net"
    "testing"
)

// mockDialContext simulates network connections. Ports 80 and 443 are considered open.
func mockDialContext(_ context.Context, network, address string) (net.Conn, error) {
    // address format: host:port
    var port int
    _, err := fmt.Sscanf(address, "%*[^:]:%d", &port)
    if err != nil {
        return nil, err
    }
    if port == 80 || port == 443 {
        // Return a dummy net.Conn that satisfies the interface.
        return &net.TCPConn{}, nil
    }
    return nil, errors.New("connection refused")
}

func TestIsPortOpen(t *testing.T) {
    // Save original and restore after test.
    originalDial := dialContext
    defer func() { dialContext = originalDial }()
    dialContext = mockDialContext

    tests := []struct {
        port     int
        expected bool
    }{
        {80, true},
        {443, true},
        {22, false},
        {8080, false},
    }

    for _, tt := range tests {
        got := isPortOpen("example.com", tt.port)
        if got != tt.expected {
            t.Fatalf("isPortOpen for port %d = %v; want %v", tt.port, got, tt.expected)
        }
    }
}
