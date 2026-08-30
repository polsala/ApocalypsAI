package main

import (
    "fmt"
    "net"
    "testing"
    "time"
)

func TestRelay(t *testing.T) {
    // Receiver that will act as the broadcast destination
    recvAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("resolve recv addr: %v", err)
    }
    recvConn, err := net.ListenUDP("udp", recvAddr)
    if err != nil {
        t.Fatalf("listen recv udp: %v", err)
    }
    defer recvConn.Close()
    recvPort := recvConn.LocalAddr().(*net.UDPAddr).Port

    // Sender socket used only to send test packets
    srcAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("resolve src addr: %v", err)
    }
    srcConn, err := net.ListenUDP("udp", srcAddr)
    if err != nil {
        t.Fatalf("listen src udp: %v", err)
    }
    defer srcConn.Close()
    srcPort := srcConn.LocalAddr().(*net.UDPAddr).Port

    // Build listen and broadcast strings for the relay
    listen := fmt.Sprintf("127.0.0.1:%d", srcPort)
    broadcast := fmt.Sprintf("127.0.0.1:%d", recvPort)

    // Start the relay in a separate goroutine
    go func() {
        if err := Relay(listen, broadcast); err != nil {
            t.Fatalf("relay error: %v", err)
        }
    }()

    // Give the relay a moment to start up
    time.Sleep(100 * time.Millisecond)

    // Send a test packet to the relay's listening address
    testMsg := []byte("post-apocalypse")
    _, err = srcConn.WriteToUDP(testMsg, &net.UDPAddr{IP: net.ParseIP("127.0.0.1"), Port: srcPort})
    if err != nil {
        t.Fatalf("send test packet: %v", err)
    }

    // Receive the forwarded packet from the broadcast socket
    recvConn.SetReadDeadline(time.Now().Add(1 * time.Second))
    buf := make([]byte, len(testMsg))
    n, _, err := recvConn.ReadFromUDP(buf)
    if err != nil {
        t.Fatalf("receive forwarded packet: %v", err)
    }
    if string(buf[:n]) != string(testMsg) {
        t.Fatalf("expected %q, got %q", testMsg, buf[:n])
    }

    // No explicit shutdown needed; test process termination will clean up.
}
