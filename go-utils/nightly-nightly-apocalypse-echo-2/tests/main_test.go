package main

import (
    "bufio"
    "fmt"
    "net"
    "testing"
    "time"
)

func TestRunServerEcho(t *testing.T) {
    addr, shutdown, err := RunServer(":0")
    if err != nil {
        t.Fatalf("RunServer error: %v", err)
    }
    defer shutdown()

    // small pause to ensure listener is ready
    time.Sleep(10 * time.Millisecond)

    conn, err := net.Dial("tcp", addr)
    if err != nil {
        t.Fatalf("Dial error: %v", err)
    }
    defer conn.Close()

    messages := []string{"hello", "world"}
    for _, msg := range messages {
        fmt.Fprintf(conn, "%s\n", msg)
    }

    scanner := bufio.NewScanner(conn)
    for i, msg := range messages {
        if !scanner.Scan() {
            t.Fatalf("expected response %d, got none", i)
        }
        got := scanner.Text()
        want := prefix + msg
        if got != want {
            t.Fatalf("unexpected echo: got %q, want %q", got, want)
        }
    }
}
