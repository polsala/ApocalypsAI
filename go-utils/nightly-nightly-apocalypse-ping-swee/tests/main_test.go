package main

import (
    "errors"
    "net"
    "sync"
    "testing"
    "time"
)

// mockDial simulates network connections.
// Mock rationale: treat any address equal to "alivehost:80" as reachable.
func mockDial(network, address string, timeout time.Duration) (net.Conn, error) {
    if address == "alivehost:80" {
        // Use net.Pipe to obtain a dummy net.Conn.
        c1, c2 := net.Pipe()
        // Close the opposite end immediately; we only need a non‑nil Conn.
        c2.Close()
        return c1, nil
    }
    return nil, errors.New("mock connection refused")
}

func TestCheckTargetAlive(t *testing.T) {
    // Replace the global dialFunc with our mock.
    originalDial := dialFunc
    dialFunc = mockDial
    defer func() { dialFunc = originalDial }()

    wg := &sync.WaitGroup{}
    ch := make(chan result, 1)
    wg.Add(1)
    go checkTarget("alivehost", wg, ch)
    wg.Wait()
    close(ch)

    r := <-ch
    if !r.alive {
        t.Fatalf("expected alive, got dead")
    }
    if r.target != "alivehost" {
        t.Fatalf("unexpected target %s", r.target)
    }
}

func TestCheckTargetDead(t *testing.T) {
    originalDial := dialFunc
    dialFunc = mockDial
    defer func() { dialFunc = originalDial }()

    wg := &sync.WaitGroup{}
    ch := make(chan result, 1)
    wg.Add(1)
    go checkTarget("deadhost", wg, ch)
    wg.Wait()
    close(ch)

    r := <-ch
    if r.alive {
        t.Fatalf("expected dead, got alive")
    }
    if r.target != "deadhost" {
        t.Fatalf("unexpected target %s", r.target)
    }
}
