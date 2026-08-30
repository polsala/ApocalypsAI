package main

import (
    "bufio"
    "net"
    "strings"
    "testing"
)

func TestHandleConnEcho(t *testing.T) {
    // Replace emojis slice with a single deterministic emoji to avoid randomness.
    originalEmojis := emojis
    emojis = []string{"🧪"}
    defer func() { emojis = originalEmojis }()

    client, server := net.Pipe()
    defer client.Close()
    defer server.Close()

    go handleConn(server)

    // Send a line to the server.
    msg := "test line"
    if _, err := client.Write([]byte(msg + "\n")); err != nil {
        t.Fatalf("write error: %v", err)
    }

    // Read the response.
    reader := bufio.NewReader(client)
    resp, err := reader.ReadString('\n')
    if err != nil {
        t.Fatalf("read error: %v", err)
    }
    resp = strings.TrimSpace(resp)

    expected := msg + " 🧪"
    if resp != expected {
        t.Fatalf("expected %q, got %q", expected, resp)
    }
}
