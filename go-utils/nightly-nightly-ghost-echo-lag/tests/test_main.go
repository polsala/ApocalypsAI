package main

import (
    "net"
    "testing"
)

func TestMeasureRTT(t *testing.T) {
    // Start a local TCP listener
    ln, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("failed to start listener: %v", err)
    }
    defer ln.Close()
    addr := ln.Addr().(*net.TCPAddr)
    // Run measureRTT
    rtt, err := measureRTT(addr.IP.String(), addr.Port)
    if err != nil {
        t.Fatalf("measureRTT returned error: %v", err)
    }
    if rtt <= 0 {
        t.Fatalf("expected positive RTT, got %v", rtt)
    }
}

func TestMeasureRTTError(t *testing.T) {
    _, err := measureRTT("10.255.255.1", 80)
    if err == nil {
        t.Fatalf("expected error for unreachable host")
    }
}
