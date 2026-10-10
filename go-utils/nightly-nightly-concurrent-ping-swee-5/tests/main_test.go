package main

import (
    "net"
    "testing"
    "time"
)

// startMockServer launches a TCP listener that accepts a connection,
// sleeps for the specified delay, then closes the connection.
// It returns the address (host:port) and a cleanup function.
func startMockServer(t *testing.T, delay time.Duration) (string, func()) {
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
            // Simulate processing delay then close.
            time.Sleep(delay)
            conn.Close()
        }
    }()
    return ln.Addr().String(), func() { ln.Close() }
}

func TestPingHosts(t *testing.T) {
    // Fast mock server (~50ms latency)
    fastAddr, closeFast := startMockServer(t, 50*time.Millisecond)
    defer closeFast()
    // Slow mock server (~200ms latency)
    slowAddr, closeSlow := startMockServer(t, 200*time.Millisecond)
    defer closeSlow()
    // Unreachable address (no server listening)
    badAddr := "127.0.0.1:9" // commonly closed port

    hosts := []string{fastAddr, slowAddr, badAddr}
    results := PingHosts(hosts, 1*time.Second, 2)

    // Fast host should have latency < 100ms and no error.
    if results[0].Error != "" && results[0].LatencyMs > 100 {
        t.Errorf("expected fast host latency <100ms, got %.2f ms, err: %s", results[0].LatencyMs, results[0].Error)
    }
    // Slow host should have latency roughly between 150ms and 300ms.
    if results[1].Error != "" && (results[1].LatencyMs < 150 || results[1].LatencyMs > 300) {
        t.Errorf("expected slow host latency ~200ms, got %.2f ms, err: %s", results[1].LatencyMs, results[1].Error)
    }
    // Bad host must report an error.
    if results[2].Error == "" {
        t.Errorf("expected error for unreachable host, got none")
    }
}
