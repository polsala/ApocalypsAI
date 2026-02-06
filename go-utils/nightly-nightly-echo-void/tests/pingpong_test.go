package main

import (
    "bufio"
    "log"
    "net"
    "strconv"
    "strings"
    "sync"
    "testing"
    "time"
)

// mockServer starts a UDP echo server on an OS‑assigned port and returns the address.
func mockServer(t *testing.T) (addr string, teardown func()) {
    t.Helper()
    // Use port 0 to let the OS pick an available port.
    udpAddr, err := net.ResolveUDPAddr("udp", ":0")
    if err != nil {
        t.Fatalf("resolve udp addr: %v", err)
    }
    conn, err := net.ListenUDP("udp", udpAddr)
    if err != nil {
        t.Fatalf("listen udp: %v", err)
    }
    // Capture the actual address (including the chosen port).
    actualAddr := conn.LocalAddr().String()
    var wg sync.WaitGroup
    wg.Add(1)
    go func() {
        defer wg.Done()
        buf := make([]byte, 4096)
        for {
            n, clientAddr, err := conn.ReadFromUDP(buf)
            if err != nil {
                // When the connection is closed, exit gracefully.
                return
            }
            payload := string(buf[:n])
            timestamp := time.Now().UnixNano()
            response := strconv.FormatInt(timestamp, 10) + ":" + payload
            _, _ = conn.WriteToUDP([]byte(response), clientAddr)
        }
    }()
    return actualAddr, func() {
        conn.Close()
        wg.Wait()
    }
}

func TestPingPongEcho(t *testing.T) {
    serverAddr, teardown := mockServer(t)
    defer teardown()

    // Use the same helper logic as the production client.
    payload, rtt, err := pingServer(serverAddr, "test-message")
    if err != nil {
        t.Fatalf("pingServer returned error: %v", err)
    }
    if payload != "test-message" {
        t.Fatalf("expected echoed payload 'test-message', got '%s'", payload)
    }
    if rtt <= 0 {
        t.Fatalf("expected positive round‑trip time, got %s", rtt)
    }
}

// Additional sanity test: ensure the server prefixes a timestamp.
func TestServerResponseFormat(t *testing.T) {
    serverAddr, teardown := mockServer(t)
    defer teardown()

    // Directly talk to the mock server without the client helper.
    udpAddr, err := net.ResolveUDPAddr("udp", serverAddr)
    if err != nil {
        t.Fatalf("resolve udp addr: %v", err)
    }
    conn, err := net.DialUDP("udp", nil, udpAddr)
    if err != nil {
        t.Fatalf("dial udp: %v", err)
    }
    defer conn.Close()

    msg := "format-test"
    _, err = conn.Write([]byte(msg))
    if err != nil {
        t.Fatalf("write udp: %v", err)
    }
    conn.SetReadDeadline(time.Now().Add(2 * time.Second))
    respBuf := make([]byte, 4096)
    n, _, err := conn.ReadFromUDP(respBuf)
    if err != nil {
        t.Fatalf("read udp: %v", err)
    }
    resp := string(respBuf[:n])
    parts := strings.SplitN(resp, ":", 2)
    if len(parts) != 2 {
        t.Fatalf("malformed response: %s", resp)
    }
    // Verify timestamp is a valid integer.
    if _, err := strconv.ParseInt(parts[0], 10, 64); err != nil {
        t.Fatalf("timestamp not integer: %v", err)
    }
    if parts[1] != msg {
        t.Fatalf("payload mismatch: expected %s, got %s", msg, parts[1])
    }
    // Suppress unused log warnings.
    log.Println("response format verified")
}
