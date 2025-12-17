package main

import (
    "net"
    "testing"
    "time"
)

func TestScanPortsDetectOpenPort(t *testing.T) {
    // Start a temporary TCP server on an OS‑assigned port.
    ln, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("failed to listen: %v", err)
    }
    defer ln.Close()
    addr := ln.Addr().(*net.TCPAddr)
    port := addr.Port

    // Run the scanner.
    done := make(chan []int, 1)
    go func() {
        open := ScanPorts("127.0.0.1", port, port, 10)
        done <- open
    }()

    select {
    case open := <-done:
        if len(open) != 1 || open[0] != port {
            t.Fatalf("expected port %d to be reported open, got %v", port, open)
        }
    case <-time.After(2 * time.Second):
        t.Fatalf("scanner timed out")
    }
}

func TestScanPortsIgnoreClosedPort(t *testing.T) {
    // Choose a high port that is unlikely to be open.
    closedPort := 54321
    open := ScanPorts("127.0.0.1", closedPort, closedPort, 5)
    if len(open) != 0 {
        t.Fatalf("expected no open ports, got %v", open)
    }
}
