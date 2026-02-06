package main

import (
    "bufio"
    "net"
    "testing"
)

func TestHandleConnectionSingleLine(t *testing.T) {
    client, server := net.Pipe()
    defer client.Close()
    defer server.Close()

    phrases := []string{"Doomsday"}
    go handleConnection(server, phrases)

    // Send a single line
    if _, err := client.Write([]byte("hello\n")); err != nil {
        t.Fatalf("write failed: %v", err)
    }

    // Read response
    resp, err := bufio.NewReader(client).ReadString('\n')
    if err != nil {
        t.Fatalf("read failed: %v", err)
    }
    expected := "Doomsday: hello\n"
    if resp != expected {
        t.Fatalf("expected %q, got %q", expected, resp)
    }
}

func TestHandleConnectionMultipleLines(t *testing.T) {
    client, server := net.Pipe()
    defer client.Close()
    defer server.Close()

    phrases := []string{"Ragnarok"}
    go handleConnection(server, phrases)

    messages := []string{"first", "second", "third"}
    for _, m := range messages {
        if _, err := client.Write([]byte(m + "\n")); err != nil {
            t.Fatalf("write failed: %v", err)
        }
        resp, err := bufio.NewReader(client).ReadString('\n')
        if err != nil {
            t.Fatalf("read failed: %v", err)
        }
        expected := "Ragnarok: " + m + "\n"
        if resp != expected {
            t.Fatalf("expected %q, got %q", expected, resp)
        }
    }
}
