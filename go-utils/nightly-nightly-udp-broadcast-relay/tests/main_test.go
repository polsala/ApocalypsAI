package main

import (
    "net"
    "testing"
    "time"
)

func TestForwardMessage(t *testing.T) {
    // Set up a mock UDP receiver
    recvConn, err := net.ListenUDP("udp", &net.UDPAddr{IP: net.ParseIP("127.0.0.1"), Port: 0})
    if err != nil {
        t.Fatalf("listen mock receiver: %v", err)
    }
    defer recvConn.Close()
    recvAddr := recvConn.LocalAddr().String()

    // Channel to capture the incoming packet
    got := make(chan []byte, 1)
    go func() {
        buf := make([]byte, 1024)
        n, _, _ := recvConn.ReadFromUDP(buf)
        got <- buf[:n]
    }()

    // Use the forwardMessage helper to send a packet to the mock receiver
    payload := []byte("beacon")
    if err := forwardMessage(recvAddr, payload); err != nil {
        t.Fatalf("forwardMessage failed: %v", err)
    }

    select {
    case data := <-got:
        if string(data) != "beacon" {
            t.Fatalf("receiver got %s, want beacon", string(data))
        }
    case <-time.After(time.Second):
        t.Fatal("timeout waiting for mock receiver")
    }
}
