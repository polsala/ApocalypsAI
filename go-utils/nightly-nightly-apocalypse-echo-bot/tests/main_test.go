package main

import (
    "bufio"
    "net"
    "strings"
    "testing"
    "time"
)

func TestEchoBot(t *testing.T) {
    // Start server on a random available port
    ln, err := net.Listen("tcp", ":0")
    if err != nil {
        t.Fatalf("failed to listen: %v", err)
    }
    defer ln.Close()

    // Run the server loop in a goroutine
    go func() {
        for {
            conn, err := ln.Accept()
            if err != nil {
                return
            }
            go handleConn(conn)
        }
    }()

    // Small pause to ensure the listener is ready
    time.Sleep(10 * time.Millisecond)

    addr := ln.Addr().String()
    conn, err := net.Dial("tcp", addr)
    if err != nil {
        t.Fatalf("dial error: %v", err)
    }
    defer conn.Close()

    msg := "Hello world"
    _, err = conn.Write([]byte(msg + "\n"))
    if err != nil {
        t.Fatalf("write error: %v", err)
    }

    reader := bufio.NewReader(conn)
    resp, err := reader.ReadString('\n')
    if err != nil {
        t.Fatalf("read error: %v", err)
    }
    resp = strings.TrimSpace(resp)

    // Expected format: "<phrase>: <msg>"
    parts := strings.SplitN(resp, ": ", 2)
    if len(parts) != 2 {
        t.Fatalf("unexpected response format: %s", resp)
    }
    phrase, echoed := parts[0], parts[1]

    // Verify the phrase is one of the predefined apocalyptic phrases
    found := false
    for _, p := range phrases {
        if p == phrase {
            found = true
            break
        }
    }
    if !found {
        t.Fatalf("phrase not recognized: %s", phrase)
    }
    if echoed != msg {
        t.Fatalf("expected echoed message %q, got %q", msg, echoed)
    }
}
