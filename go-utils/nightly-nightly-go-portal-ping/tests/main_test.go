package main

import (
    "net"
    "testing"
    "time"
)

func TestPingHosts(t *testing.T) {
    // Start a dummy TCP server listening on an OSâassigned port
    ln, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("failed to start listener: %v", err)
    }
    defer ln.Close()
    addr := ln.Addr().String()

    // Prepare host list: one reachable, one expected to fail
    hosts := []string{addr, "127.0.0.1:9"} // port 9 is typically closed
    results := pingHosts(hosts, 500*time.Millisecond)

    if len(results) != 2 {
        t.Fatalf("expected 2 results, got %d", len(results))
    }

    // First host should succeed
    if results[0].Err != nil {
        t.Errorf("expected first host to succeed, got error: %v", results[0].Err)
    }
    // Second host should fail
    if results[1].Err == nil {
        t.Errorf("expected second host to fail, but got success")
    }
}

