package main

import (
    "net"
    "testing"
    "time"
)

// startEchoServer launches a UDP server that echoes any received payload.
// It returns the listening address and a function to shut it down.
func startEchoServer(t *testing.T) (addr *net.UDPAddr, closeFn func()) {
    t.Helper()
    laddr, err := net.ResolveUDPAddr("udp", "127.0.0.1:0") // OS‑assigned port
    if err != nil {
        t.Fatalf("resolve udp addr: %v", err)
    }
    conn, err := net.ListenUDP("udp", laddr)
    if err != nil {
        t.Fatalf("listen udp: %v", err)
    }
    go func() {
        buf := make([]byte, 1024)
        for {
            n, remote, err := conn.ReadFromUDP(buf)
            if err != nil {
                return // closed
            }
            _, _ = conn.WriteToUDP(buf[:n], remote) // echo back
        }
    }()
    return conn.LocalAddr().(*net.UDPAddr), func() { conn.Close() }
}

func TestPingHostSuccess(t *testing.T) {
    addr, closeSrv := startEchoServer(t)
    defer closeSrv()

    result := PingHost(addr.String(), "testmsg", 2*time.Second)
    if result.Err != nil {
        t.Fatalf("expected no error, got %v", result.Err)
    }
    if result.RTT <= 0 {
        t.Fatalf("expected positive RTT, got %v", result.RTT)
    }
    // Message integrity is verified inside PingHost; no further check needed.
}

func TestPingHostTimeout(t *testing.T) {
    // Use an address that does not have a listener to trigger timeout.
    result := PingHost("127.0.0.1:9", "msg", 500*time.Millisecond)
    if result.Err == nil {
        t.Fatalf("expected timeout error, got nil")
    }
}
