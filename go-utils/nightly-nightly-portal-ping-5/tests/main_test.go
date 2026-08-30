package main

import (
    "net"
    "testing"
)

func TestScanPorts_OpenPort(t *testing.T) {
    // Mock rationale: start a real TCP listener to act as an open port.
    ln, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("failed to listen: %v", err)
    }
    defer ln.Close()
    addr := ln.Addr().(*net.TCPAddr)
    port := addr.Port

    ports := []int{port}
    open := ScanPorts("127.0.0.1", ports, 5)
    if len(open) != 1 || open[0] != port {
        t.Fatalf("expected port %d to be reported open, got %v", port, open)
    }
}

func TestScanPorts_ClosedPort(t *testing.T) {
    // Mock rationale: pick a high-numbered port unlikely to be open.
    closedPort := 65535
    ports := []int{closedPort}
    open := ScanPorts("127.0.0.1", ports, 5)
    if len(open) != 0 {
        t.Fatalf("expected no open ports, got %v", open)
    }
}
