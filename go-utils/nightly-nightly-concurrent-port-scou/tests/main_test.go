package main

import (
    "net"
    "testing"
    "time"
)

// startTempListener starts a TCP listener on a random available port and returns the listener and its port.
func startTempListener(t *testing.T) (net.Listener, int) {
    ln, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("failed to start temporary listener: %v", err)
    }
    addr := ln.Addr().(*net.TCPAddr)
    return ln, addr.Port
}

func TestScanPortsDetectsOpenAndClosed(t *testing.T) {
    // Mock rationale: start two listeners to represent open ports, pick a closed port far away.
    ln1, port1 := startTempListener(t)
    defer ln1.Close()
    ln2, port2 := startTempListener(t)
    defer ln2.Close()

    closedPort := 65000 // unlikely to be open during test
    ports := []int{port1, port2, closedPort}

    open := ScanPorts("127.0.0.1", ports, 5, 100*time.Millisecond)

    if len(open) != 2 {
        t.Fatalf("expected 2 open ports, got %d", len(open))
    }
    found := map[int]bool{port1: false, port2: false}
    for _, p := range open {
        if _, ok := found[p]; ok {
            found[p] = true
        } else {
            t.Fatalf("unexpected open port reported: %d", p)
        }
    }
    for p, ok := range found {
        if !ok {
            t.Fatalf("open port %d was not reported", p)
        }
    }
}
