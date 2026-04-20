package main

import (
    "fmt"
    "net"
    "testing"
    "time"
)

func TestRunScanner(t *testing.T) {
    // Save the original dialFunc and restore after the test.
    originalDial := dialFunc
    defer func() { dialFunc = originalDial }()

    // Mock implementation: succeed only for "good.com:80".
    dialFunc = func(network, address string, timeout time.Duration) (net.Conn, error) {
        if address == "good.com:80" {
            // Use net.Pipe to obtain a dummy net.Conn.
            c1, c2 := net.Pipe()
            // Close the opposite end immediately; we only need a Conn that can be closed.
            c2.Close()
            return c1, nil
        }
        return nil, fmt.Errorf("mock failure")
    }

    inputs := []string{"good.com:80", "bad.com:1234"}
    results := runScanner(inputs, 1*time.Second, 2)

    expected := []string{
        "Signal received from good.com:80",
        "No signal from bad.com:1234",
    }

    for i, exp := range expected {
        if results[i] != exp {
            t.Fatalf("expected %q, got %q at index %d", exp, results[i], i)
        }
    }
}
