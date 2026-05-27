package main

import (
    "bufio"
    "fmt"
    "math/rand"
    "net"
    "os"
    "strings"
    "testing"
    "time"
)

// startTestServer launches the server in a goroutine on the given port.
func startTestServer(t *testing.T, port string) {
    // Override os.Args to simulate command‑line argument for port.
    origArgs := os.Args
    os.Args = []string{"cmd", port}
    go func() {
        main()
    }()
    // Restore original args after test.
    os.Args = origArgs
    // Give the server a moment to start listening.
    time.Sleep(200 * time.Millisecond)
}

func TestEchoPrefix(t *testing.T) {
    port := "9090"
    startTestServer(t, port)

    conn, err := net.Dial("tcp", "127.0.0.1:"+port)
    if err != nil {
        t.Fatalf("dial failed: %v", err)
    }
    defer conn.Close()

    msg := "Hello apocalypse"
    fmt.Fprintf(conn, "%s\n", msg)

    reader := bufio.NewReader(conn)
    line, err := reader.ReadString('\n')
    if err != nil {
        t.Fatalf("read failed: %v", err)
    }
    line = strings.TrimSpace(line)

    // Re‑seed with the same value to predict the prefix.
    rand.Seed(42)
    expectedPrefix := getPrefix()
    expected := fmt.Sprintf("%s %s", expectedPrefix, msg)
    if line != expected {
        t.Fatalf("expected %q, got %q", expected, line)
    }
}
