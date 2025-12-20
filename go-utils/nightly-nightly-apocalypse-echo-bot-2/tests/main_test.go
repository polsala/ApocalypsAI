package main

import (
    "bufio"
    "math/rand"
    "net"
    "strings"
    "testing"
    "time"
)

func init() {
    // Ensure deterministic random choices in tests
    rand.Seed(42)
}

func startTestServer(t *testing.T) (addr string, closeFunc func()) {
    ln, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("Failed to listen: %v", err)
    }
    go func() {
        for {
            conn, err := ln.Accept()
            if err != nil {
                return
            }
            go handleConn(conn)
        }
    }()
    return ln.Addr().String(), func() { ln.Close() }
}

func TestEchoResponse(t *testing.T) {
    addr, closeSrv := startTestServer(t)
    defer closeSrv()

    // give server a moment to start
    time.Sleep(10 * time.Millisecond)

    conn, err := net.Dial("tcp", addr)
    if err != nil {
        t.Fatalf("Dial error: %v", err)
    }
    defer conn.Close()

    msg := "Hello World"
    _, err = conn.Write([]byte(msg + "\n"))
    if err != nil {
        t.Fatalf("Write error: %v", err)
    }

    reader := bufio.NewReader(conn)
    resp, err := reader.ReadString('\n')
    if err != nil {
        t.Fatalf("Read error: %v", err)
    }
    resp = strings.TrimSpace(resp)

    expectedPrefix := "[The Skies Crack]"
    if !strings.HasPrefix(resp, expectedPrefix) {
        t.Fatalf("Expected prefix %s, got %s", expectedPrefix, resp)
    }
    if !strings.HasSuffix(resp, msg) {
        t.Fatalf("Expected message suffix %s, got %s", msg, resp)
    }
}
