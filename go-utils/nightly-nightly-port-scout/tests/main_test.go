package main

import (
    "net"
    "sort"
    "testing"
    "time"
)

// startTempListener starts a TCP listener on a random port and returns the port number and a close function.
func startTempListener(t *testing.T) (int, func()) {
    ln, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("failed to start listener: %v", err)
    }
    addr := ln.Addr().(*net.TCPAddr)
    closeFn := func() { ln.Close() }
    return addr.Port, closeFn
}

func TestScanPorts(t *testing.T) {
    // Mock rationale: start two open ports and one closed port to verify detection.
    openPort1, close1 := startTempListener(t)
    defer close1()
    openPort2, close2 := startTempListener(t)
    defer close2()

    closedPort := openPort2 + 1000 // unlikely to be open
    ports := []int{openPort1, openPort2, closedPort}

    timeout := 200 * time.Millisecond
    maxWorkers := 10
    open := ScanPorts("127.0.0.1", ports, timeout, maxWorkers)

    // Ensure the result contains exactly the two open ports.
    expected := []int{openPort1, openPort2}
    sort.Ints(open)
    sort.Ints(expected)
    if len(open) != len(expected) {
        t.Fatalf("expected %d open ports, got %d", len(expected), len(open))
    }
    for i, p := range expected {
        if open[i] != p {
            t.Fatalf("expected port %d at index %d, got %d", p, i, open[i])
        }
    }
}
