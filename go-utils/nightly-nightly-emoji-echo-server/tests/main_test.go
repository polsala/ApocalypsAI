package main

import (
    "bufio"
    "net"
    "os"
    "strings"
    "testing"
    "time"
)

func TestEmojiEchoServer(t *testing.T) {
    // Ensure deterministic randomness
    os.Setenv("SEED", "42")
    defer os.Unsetenv("SEED")

    // Listen on a random free port
    listener, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("Failed to listen: %v", err)
    }
    defer listener.Close()

    // Start server in background
    go func() {
        // # Mock rationale: startServer runs accept loop; we ignore its error on listener close.
        _ = startServer(listener)
    }()

    // Give the server a moment to start
    time.Sleep(10 * time.Millisecond)

    // Connect as client
    conn, err := net.Dial("tcp", listener.Addr().String())
    if err != nil {
        t.Fatalf("Failed to connect to server: %v", err)
    }
    defer conn.Close()

    // Send a line
    msg := "hello world"
    fmt.Fprintf(conn, "%s\n", msg)

    // Read response
    reader := bufio.NewReader(conn)
    resp, err := reader.ReadString('\n')
    if err != nil {
        t.Fatalf("Failed to read response: %v", err)
    }
    resp = strings.TrimSpace(resp)

    // Verify format "<msg> <emoji>"
    parts := strings.SplitN(resp, " ", 2)
    if len(parts) != 2 {
        t.Fatalf("Unexpected response format: %s", resp)
    }
    if parts[0] != msg {
        t.Fatalf("Message mismatch: got %s, want %s", parts[0], msg)
    }
    emoji := parts[1]
    // Check emoji is one of the allowed set
    allowed := map[string]bool{"😀": true, "😂": true, "😎": true, "🤖": true, "👾": true}
    if !allowed[emoji] {
        t.Fatalf("Unexpected emoji %s; allowed set %v", emoji, allowed)
    }
}
