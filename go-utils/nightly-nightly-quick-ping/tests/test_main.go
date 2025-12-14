package main

import (
    "net"
    "testing"
    "time"
)

func TestPingSuccess(t *testing.T) {
    // Start a local TCP server
    ln, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("Failed to start listener: %v", err)
    }
    defer ln.Close()
    addr := ln.Addr().(*net.TCPAddr)
    host := addr.IP.String()
    port := addr.Port

    // Run ping
    res := ping(host, port, 2*time.Second)
    if !res.Success {
        t.Fatalf("Expected success, got error: %s", res.Error)
    }
    if res.Latency == "" {
        t.Fatalf("Expected latency, got empty")
    }
}

func TestPingFailure(t *testing.T) {
    // Use a port that is unlikely to be open
    host := "127.0.0.1"
    port := 65535 // usually closed
    res := ping(host, port, 1*time.Second)
    if res.Success {
        t.Fatalf("Expected failure, got success")
    }
    if res.Error == "" {
        t.Fatalf("Expected error message")
    }
}
