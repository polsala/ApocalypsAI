package main

import (
    "bufio"
    "fmt"
    "math/rand"
    "net"
    "strings"
    "testing"
    "time"
)

// Helper to check if a string is in the slice of phrases.
func containsPhrase(s string) bool {
    for _, p := range phrases {
        if strings.HasPrefix(s, p+" ") {
            return true
        }
    }
    return false
}

func TestFormatMessage(t *testing.T) {
    // Use a deterministic random source.
    r := rand.New(rand.NewSource(42))
    msg := "Hello World"
    out := formatMessage(msg, r)
    if !strings.Contains(out, msg) {
        t.Fatalf("output does not contain original message: %s", out)
    }
    if !containsPhrase(out) {
        t.Fatalf("output does not start with a known phrase: %s", out)
    }
}

func TestHandleConnection(t *testing.T) {
    // Create a deterministic random source with a fixed seed.
    r := rand.New(rand.NewSource(99))

    client, server := net.Pipe()
    defer client.Close()
    defer server.Close()

    // Run the server side handler in a goroutine.
    go handleConnection(server, r)

    // Simulate client sending a line.
    fmt.Fprintln(client, "test message")

    // Read the response.
    reader := bufio.NewReader(client)
    resp, err := reader.ReadString('\n')
    if err != nil {
        t.Fatalf("failed to read response: %v", err)
    }
    resp = strings.TrimSpace(resp)

    if !strings.Contains(resp, "test message") {
        t.Fatalf("response does not contain original message: %s", resp)
    }
    if !containsPhrase(resp) {
        t.Fatalf("response does not start with a known phrase: %s", resp)
    }
}

// Ensure the test suite runs quickly; we set a timeout.
func TestMain(m *testing.M) {
    // Limit total test time to avoid hanging.
    timeout := time.AfterFunc(5*time.Second, func() {
        fmt.Println("Tests timed out")
        os.Exit(1)
    })
    code := m.Run()
    timeout.Stop()
    os.Exit(code)
}
