package main

import (
    "bufio"
    "net"
    "strings"
    "testing"
    "time"
)

func TestServerEcho(t *testing.T) {
    // Use a deterministic tag list for the test.
    SetTags([]string{"[Doom]", "[Ashes]"})

    // Start server on an OS‑assigned port.
    ln, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("failed to listen: %v", err)
    }
    defer ln.Close()

    // Run server loop in background.
    go func() {
        for {
            conn, err := ln.Accept()
            if err != nil {
                return // Listener closed.
            }
            go handleConn(conn)
        }
    }()

    // Give the goroutine a moment to start.
    time.Sleep(10 * time.Millisecond)

    // Connect as a client.
    conn, err := net.Dial("tcp", ln.Addr().String())
    if err != nil {
        t.Fatalf("dial error: %v", err)
    }
    defer conn.Close()

    rw := bufio.NewReadWriter(bufio.NewReader(conn), bufio.NewWriter(conn))

    // Helper to send a line and read response.
    sendAndRecv := func(msg string) string {
        fmt.Fprintf(rw, "%s\n", msg)
        rw.Flush()
        resp, err := rw.ReadString('\n')
        if err != nil {
            t.Fatalf("read error: %v", err)
        }
        return strings.TrimSpace(resp)
    }

    // First message should get the first tag.
    if got := sendAndRecv("hello"); got != "[Doom] hello" {
        t.Fatalf("expected '[Doom] hello', got %q", got)
    }
    // Second message should rotate to the next tag.
    if got := sendAndRecv("world"); got != "[Ashes] world" {
        t.Fatalf("expected '[Ashes] world', got %q", got)
    }
    // Third message wraps around to the first tag again.
    if got := sendAndRecv("again"); got != "[Doom] again" {
        t.Fatalf("expected '[Doom] again', got %q", got)
    }
}
