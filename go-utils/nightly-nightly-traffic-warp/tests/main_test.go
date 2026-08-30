package main

import (
    "bytes"
    "math/rand"
    "net"
    "testing"
    "time"
)

func TestCopyWithEffects_NoLoss_NoJitter(t *testing.T) {
    rand.Seed(42) // deterministic

    cfg := Config{
        latency: 10 * time.Millisecond,
        jitter:  0,
        loss:    0.0,
    }

    client, server := net.Pipe()
    defer client.Close()
    defer server.Close()

    go copyWithEffects(client, server, cfg)

    msg := []byte("hello world")
    start := time.Now()
    _, err := server.Write(msg)
    if err != nil {
        t.Fatalf("write error: %v", err)
    }

    buf := make([]byte, len(msg))
    n, err := client.Read(buf)
    if err != nil {
        t.Fatalf("read error: %v", err)
    }
    elapsed := time.Since(start)

    if !bytes.Equal(buf[:n], msg) {
        t.Fatalf("expected %s, got %s", msg, buf[:n])
    }
    if elapsed < cfg.latency {
        t.Fatalf("expected at least %v latency, got %v", cfg.latency, elapsed)
    }
}

func TestCopyWithEffects_FullLoss(t *testing.T) {
    rand.Seed(42)

    cfg := Config{
        latency: 0,
        jitter:  0,
        loss:    1.0, // 100% loss
    }

    client, server := net.Pipe()
    defer client.Close()
    defer server.Close()

    go copyWithEffects(client, server, cfg)

    msg := []byte("should be lost")
    _, err := server.Write(msg)
    if err != nil {
        t.Fatalf("write error: %v", err)
    }

    client.SetReadDeadline(time.Now().Add(50 * time.Millisecond))
    buf := make([]byte, 1024)
    _, err = client.Read(buf)
    if err == nil {
        t.Fatalf("expected timeout or no data due to loss, but data was received")
    }
    // Expected timeout due to loss
}
