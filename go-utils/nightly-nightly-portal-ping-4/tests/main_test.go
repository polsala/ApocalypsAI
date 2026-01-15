package main

import (
    "net"
    "testing"
    "time"
)

func TestPingHostSuccess(t *testing.T) {
    // Start a mock TCP server on an OS‑assigned port.
    ln, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("listen error: %v", err)
    }
    defer ln.Close()
    go func() {
        for {
            conn, err := ln.Accept()
            if err != nil {
                return
            }
            conn.Close()
        }
    }()
    addr := ln.Addr().String()
    dur, err := PingHost(addr, 1*time.Second)
    if err != nil {
        t.Fatalf("expected no error, got %v", err)
    }
    if dur <= 0 {
        t.Fatalf("expected positive duration, got %v", dur)
    }
}

func TestPingHostTimeout(t *testing.T) {
    // Use a non‑routable address to force a timeout.
    _, err := PingHost("10.255.255.1:12345", 100*time.Millisecond)
    if err == nil {
        t.Fatalf("expected timeout error")
    }
}

func TestPingMultiple(t *testing.T) {
    // First mock server.
    ln1, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("listen error: %v", err)
    }
    defer ln1.Close()
    go func() {
        for {
            c, err := ln1.Accept()
            if err != nil {
                return
            }
            c.Close()
        }
    }()
    // Second mock server.
    ln2, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("listen error: %v", err)
    }
    defer ln2.Close()
    go func() {
        for {
            c, err := ln2.Accept()
            if err != nil {
                return
            }
            c.Close()
        }
    }()
    hosts := []string{ln1.Addr().String(), ln2.Addr().String(), "10.255.255.1:12345"}
    results := PingMultiple(hosts, 200*time.Millisecond)
    for _, h := range hosts {
        dur := results[h]
        if h == "10.255.255.1:12345" {
            if dur >= 0 {
                t.Fatalf("expected unreachable for %s", h)
            }
        } else {
            if dur <= 0 {
                t.Fatalf("expected positive duration for %s", h)
            }
        }
    }
}
