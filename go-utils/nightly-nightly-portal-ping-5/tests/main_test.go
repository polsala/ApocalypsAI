package main

import (
    "net"
    "testing"
    "time"
)

// startTestListener starts a TCP server on a random free port and returns the listener and its port.
func startTestListener(t *testing.T) (net.Listener, int) {
    ln, err := net.Listen("tcp", "127.0.0.1:0") // OS chooses a free port
    if err != nil {
        t.Fatalf("failed to start test listener: %v", err)
    }
    addr := ln.Addr().(*net.TCPAddr)
    return ln, addr.Port
}

func TestScanPorts_OpenAndClosed(t *testing.T) {
    // Mock rationale: we create a real listener for the "open" port and rely on the OS to refuse connections on an adjacent port.
    ln, openPort := startTestListener(t)
    defer ln.Close()

    closedPort := openPort + 1 // assume this port is free; deterministic because we never bind to it.
    ports := []int{openPort, closedPort}

    results := ScanPorts("127.0.0.1", ports, 2, 100*time.Millisecond)
    if len(results) != 2 {
        t.Fatalf("expected 2 results, got %d", len(results))
    }
    // Verify open port detected
    if !results[0].Open {
        t.Errorf("expected port %d to be open", openPort)
    }
    // Verify closed port detected
    if results[1].Open {
        t.Errorf("expected port %d to be closed", closedPort)
    }
}

func TestParsePortRange(t *testing.T) {
    cases := []struct {
        input    string
        expected []int
        wantErr  bool
    }{
        {"8000-8002", []int{8000, 8001, 8002}, false},
        {"1-3", []int{1, 2, 3}, false},
        {"5-5", []int{5}, false},
        {"10-5", nil, true},
        {"abc-def", nil, true},
    }
    for _, c := range cases {
        got, err := parsePortRange(c.input)
        if c.wantErr {
            if err == nil {
                t.Errorf("expected error for input %s, got none", c.input)
            }
            continue
        }
        if err != nil {
            t.Errorf("unexpected error for input %s: %v", c.input, err)
            continue
        }
        if len(got) != len(c.expected) {
            t.Errorf("input %s: expected %d ports, got %d", c.input, len(c.expected), len(got))
            continue
        }
        for i := range got {
            if got[i] != c.expected[i] {
                t.Errorf("input %s: expected port %d at index %d, got %d", c.input, c.expected[i], i, got[i])
            }
        }
    }
}
