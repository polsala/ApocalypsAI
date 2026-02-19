package main

import (
    "net"
    "testing"
    "time"
)

func TestUDPServerEcho(t *testing.T) {
    // Start a UDP listener on a random port (acts as the server)
    udpAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("resolve: %v", err)
    }
    serverConn, err := net.ListenUDP("udp", udpAddr)
    if err != nil {
        t.Fatalf("listen: %v", err)
    }
    defer serverConn.Close()
    actualAddr := serverConn.LocalAddr().String()

    // Run echo loop in background
    go func() {
        buf := make([]byte, 1024)
        for {
            n, remote, err := serverConn.ReadFromUDP(buf)
            if err != nil {
                return
            }
            serverConn.WriteToUDP(buf[:n], remote)
        }
    }()

    // Client side
    clientConn, err := net.DialUDP("udp", nil, func() *net.UDPAddr {
        a, _ := net.ResolveUDPAddr("udp", actualAddr)
        return a
    }())
    if err != nil {
        t.Fatalf("dial: %v", err)
    }
    defer clientConn.Close()

    payload := []byte("test-message")
    start := time.Now()
    _, err = clientConn.Write(payload)
    if err != nil {
        t.Fatalf("write: %v", err)
    }
    buf := make([]byte, len(payload))
    clientConn.SetReadDeadline(time.Now().Add(2 * time.Second))
    n, _, err := clientConn.ReadFromUDP(buf)
    if err != nil {
        t.Fatalf("read: %v", err)
    }
    rtt := time.Since(start)
    if string(buf[:n]) != string(payload) {
        t.Fatalf("expected echo %s, got %s", payload, buf[:n])
    }
    if rtt <= 0 {
        t.Fatalf("invalid RTT measured")
    }
}
