package main

import (
    "fmt"
    "net"
    "testing"
    "time"
)

func TestScanPorts(t *testing.T) {
    // Mock rationale: start two temporary listeners on random ports to simulate open ports.
    l1, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("failed to listen: %v", err)
    }
    defer l1.Close()
    l2, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("failed to listen: %v", err)
    }
    defer l2.Close()

    // Extract ports from the listeners.
    _, portStr1, _ := net.SplitHostPort(l1.Addr().String())
    _, portStr2, _ := net.SplitHostPort(l2.Addr().String())
    var p1, p2 int
    fmt.Sscanf(portStr1, "%d", &p1)
    fmt.Sscanf(portStr2, "%d", &p2)

    // Define a range that includes both ports.
    start := p1 - 1
    end := p2 + 1

    open := ScanPorts("127.0.0.1", start, end, 200*time.Millisecond, 50)

    // Verify both ports are detected.
    foundP1, foundP2 := false, false
    for _, p := range open {
        if p == p1 {
            foundP1 = true
        }
        if p == p2 {
            foundP2 = true
        }
    }
    if !foundP1 || !foundP2 {
        t.Fatalf("expected ports %d and %d to be open, got %v", p1, p2, open)
    }
}
