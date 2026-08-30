package main

import (
    "net"
    "testing"
    "time"
)

// Helper to start a temporary TCP listener on an available port.
func startTestListener(t *testing.T) (int, func()) {
    ln, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("failed to start listener: %v", err)
    }
    // Extract the chosen port.
    addr := ln.Addr().(*net.TCPAddr)
    port := addr.Port
    // Close function to clean up after test.
    closeFn := func() { ln.Close() }
    return port, closeFn
}

func TestScanPortsDetectsOpenPort(t *testing.T) {
    openPort, closeFn := startTestListener(t)
    defer closeFn()

    // Choose a port that is guaranteed to be closed.
    closedPort := openPort + 1

    ports := []int{openPort, closedPort}
    open := ScanPorts("127.0.0.1", ports, 200*time.Millisecond)

    if len(open) != 1 {
        t.Fatalf("expected exactly one open port, got %d", len(open))
    }
    if open[0] != openPort {
        t.Fatalf("expected open port %d, got %d", openPort, open[0])
    }
}

func TestScanPortsEmptyInput(t *testing.T) {
    open := ScanPorts("127.0.0.1", []int{}, 200*time.Millisecond)
    if len(open) != 0 {
        t.Fatalf("expected no open ports for empty input, got %d", len(open))
    }
}
