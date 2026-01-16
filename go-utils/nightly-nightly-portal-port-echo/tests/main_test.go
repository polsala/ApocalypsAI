package main

import (
    "net"
    "sort"
    "testing"
)

func TestScanPorts(t *testing.T) {
    // Start a temporary TCP listener on a random port
    ln, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("failed to listen: %v", err)
    }
    defer ln.Close()
    openPort := ln.Addr().(*net.TCPAddr).Port

    // Choose a closed port (one higher, unlikely to be open)
    closedPort := openPort + 1

    ports := scanPorts("127.0.0.1", openPort, closedPort, 10)

    // Ensure the open port is detected
    found := false
    for _, p := range ports {
        if p == openPort {
            found = true
            break
        }
    }
    if !found {
        t.Errorf("expected open port %d to be detected", openPort)
    }

    // Ensure the closed port is not reported
    for _, p := range ports {
        if p == closedPort {
            t.Errorf("closed port %d was incorrectly reported as open", closedPort)
        }
    }

    // Verify ports are sorted
    if !sort.IntsAreSorted(ports) {
        t.Errorf("ports slice is not sorted")
    }
}
