package main

import (
    "bufio"
    "math/rand"
    "net"
    "testing"
)

func TestBroadcastDeterministic(t *testing.T) {
    // Create an in‑memory connection pair.
    client, server := net.Pipe()
    defer client.Close()
    defer server.Close()

    // Two RNGs with the same seed – one for generating the expected output,
    // the other will be used by the broadcast function.
    seed := int64(42)
    rngExpected := rand.New(rand.NewSource(seed))
    rngBroadcast := rand.New(rand.NewSource(seed))

    // Build the expected slice of messages.
    expected := make([]string, 0, 10)
    for i := 0; i < 10; i++ {
        expected = append(expected, messages[rngExpected.Intn(len(messages))])
    }

    // Run the broadcaster in a separate goroutine.
    go broadcast(server, rngBroadcast)

    // Read exactly 10 lines from the client side.
    scanner := bufio.NewScanner(client)
    var received []string
    for scanner.Scan() {
        received = append(received, scanner.Text())
        if len(received) == 10 {
            break
        }
    }
    if err := scanner.Err(); err != nil {
        t.Fatalf("scanner error: %v", err)
    }

    // Compare the deterministic output.
    for i := 0; i < 10; i++ {
        if received[i] != expected[i] {
            t.Fatalf("line %d mismatch: got %q, want %q", i, received[i], expected[i])
        }
    }
}
