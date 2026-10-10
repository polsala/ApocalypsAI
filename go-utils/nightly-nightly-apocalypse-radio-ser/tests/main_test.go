package main

import (
    "bufio"
    "math/rand"
    "net"
    "strings"
    "testing"
    "time"
)

// TestGetRandomQuote ensures the function returns a quote that exists in the slice.
func TestGetRandomQuote(t *testing.T) {
    // Mock rationale: deterministic seed for reproducibility.
    rand.Seed(42)
    quote := getRandomQuote()
    found := false
    for _, q := range quotes {
        if q == quote {
            found = true
            break
        }
    }
    if !found {
        t.Fatalf("quote not found in slice: %s", quote)
    }
}

// TestServerClientInteraction starts the server on a random port, connects a client, and reads a single quote.
func TestServerClientInteraction(t *testing.T) {
    // Use a short interval to keep the test fast.
    interval := 10 * time.Millisecond
    // Start listener on an OS‑assigned port.
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
                return // listener closed
            }
            go handleClient(conn, interval)
        }
    }()

    // Connect a client.
    conn, err := net.Dial("tcp", ln.Addr().String())
    if err != nil {
        t.Fatalf("dial error: %v", err)
    }
    defer conn.Close()

    // Read the first line (quote).
    reader := bufio.NewReader(conn)
    line, err := reader.ReadString('\n')
    if err != nil {
        t.Fatalf("read error: %v", err)
    }
    line = strings.TrimSpace(line)
    if line == "" {
        t.Fatalf("received empty quote")
    }
    // Verify the received line is one of the known quotes.
    found := false
    for _, q := range quotes {
        if strings.TrimSpace(q) == line {
            found = true
            break
        }
    }
    if !found {
        t.Fatalf("received unknown quote: %s", line)
    }
}
