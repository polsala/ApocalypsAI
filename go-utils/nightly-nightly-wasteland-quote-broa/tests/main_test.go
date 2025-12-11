package main

import (
    "bufio"
    "math/rand"
    "net"
    "strconv"
    "strings"
    "testing"
    "time"
)

// Test that getRandomQuote returns deterministic results when the RNG is seeded.
func TestGetRandomQuoteDeterministic(t *testing.T) {
    seed := int64(42)
    rng := rand.New(rand.NewSource(seed))
    first := getRandomQuote(rng)
    // Reset RNG to same seed and expect the same quote.
    rng = rand.New(rand.NewSource(seed))
    second := getRandomQuote(rng)
    if first != second {
        t.Fatalf("expected deterministic quotes, got %q and %q", first, second)
    }
}

// Test a full server‑client interaction using a real UDP socket on localhost.
func TestServerClientInteraction(t *testing.T) {
    // Use a fixed seed so we know which quote to expect.
    seed := int64(12345)
    rng := rand.New(rand.NewSource(seed))
    expectedQuote := getRandomQuote(rng)

    // Start a UDP server on an OS‑assigned port (port 0).
    addr, err := net.ResolveUDPAddr("udp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("resolve udp addr: %v", err)
    }
    serverConn, err := net.ListenUDP("udp", addr)
    if err != nil {
        t.Fatalf("listen udp: %v", err)
    }
    defer serverConn.Close()

    // Extract the actual port assigned.
    _, portStr, err := net.SplitHostPort(serverConn.LocalAddr().String())
    if err != nil {
        t.Fatalf("split host port: %v", err)
    }
    port, _ := strconv.Atoi(portStr)

    // Run the server logic in a goroutine.
    go func() {
        // Re‑seed the RNG inside the server to match the test's expectation.
        serverRNG := rand.New(rand.NewSource(seed))
        // Simple loop that handles a single request then exits.
        buf := make([]byte, 1024)
        n, clientAddr, err := serverConn.ReadFromUDP(buf)
        if err != nil {
            t.Fatalf("server read error: %v", err)
        }
        _ = n // request payload ignored
        quote := getRandomQuote(serverRNG)
        _, err = serverConn.WriteToUDP([]byte(quote), clientAddr)
        if err != nil {
            t.Fatalf("server write error: %v", err)
        }
    }()

    // Give the server a moment to start.
    time.Sleep(10 * time.Millisecond)

    // Client side: send empty packet and read response.
    clientAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1:"+strconv.Itoa(port))
    if err != nil {
        t.Fatalf("resolve client addr: %v", err)
    }
    clientConn, err := net.DialUDP("udp", nil, clientAddr)
    if err != nil {
        t.Fatalf("dial udp: %v", err)
    }
    defer clientConn.Close()

    // Send request.
    _, err = clientConn.Write([]byte{})
    if err != nil {
        t.Fatalf("client write: %v", err)
    }

    // Read response.
    clientConn.SetReadDeadline(time.Now().Add(2 * time.Second))
    resp := make([]byte, 1024)
    n, _, err := clientConn.ReadFromUDP(resp)
    if err != nil {
        t.Fatalf("client read: %v", err)
    }
    received := strings.TrimSpace(string(resp[:n]))
    if received != expectedQuote {
        t.Fatalf("expected quote %q, got %q", expectedQuote, received)
    }
}
