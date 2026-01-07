package main

import (
    "net"
    "testing"
    "time"
)

// startMockServer launches a temporary TCP listener on a random port.
// It returns the address (host:port) and a function to shut it down.
func startMockServer(t *testing.T) (addr string, closeFn func()) {
    ln, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("failed to start mock server: %v", err)
    }
    go func() {
        for {
            conn, err := ln.Accept()
            if err != nil {
                return // listener closed
            }
            conn.Close()
        }
    }()
    return ln.Addr().String(), func() { ln.Close() }
}

func TestPingHostSuccess(t *testing.T) {
    addr, closeFn := startMockServer(t)
    defer closeFn()

    res := pingHost(addr, 500*time.Millisecond)
    if !res.Success {
        t.Fatalf("expected success, got error: %s", res.Error)
    }
    if res.Latency <= 0 {
        t.Fatalf("expected positive latency, got %f", res.Latency)
    }
}

func TestPingHostTimeoutOrRefused(t *testing.T) {
    // Choose a high, likely unused port on localhost.
    // The connection should be refused quickly; we treat any failure as expected.
    res := pingHost("127.0.0.1:9", 200*time.Millisecond)
    if res.Success {
        t.Fatalf("expected failure for closed port, got success")
    }
    if res.Error == "" {
        t.Fatalf("expected an error message for failed connection")
    }
}
