package main

import (
    "errors"
    "net"
    "testing"
    "time"
)

// mockDialer returns a connection after a fixed delay or an error.
func mockDialer(delay time.Duration, err error) DialerFunc {
    return func(network, address string, timeout time.Duration) (net.Conn, error) {
        if err != nil {
            return nil, err
        }
        // Simulate network latency.
        time.Sleep(delay)
        // Return a dummy net.Conn implementation.
        return &net.TCPConn{}, nil
    }
}

func TestPingHostSuccess(t *testing.T) {
    // Mock a 50ms latency.
    delay := 50 * time.Millisecond
    result := pingHost("example.com", 1*time.Second, mockDialer(delay, nil))
    if result.Err != nil {
        t.Fatalf("expected no error, got %v", result.Err)
    }
    // Allow small variance due to scheduling.
    if result.Latency < delay || result.Latency > delay+20*time.Millisecond {
        t.Fatalf("expected latency around %v, got %v", delay, result.Latency)
    }
    if result.Host != "example.com" {
        t.Fatalf("unexpected host: %s", result.Host)
    }
}

func TestPingHostError(t *testing.T) {
    mockErr := errors.New("dial timeout")
    result := pingHost("unreachable.local", 1*time.Second, mockDialer(0, mockErr))
    if result.Err == nil {
        t.Fatalf("expected error, got nil")
    }
    if !errors.Is(result.Err, mockErr) {
        t.Fatalf("expected error %v, got %v", mockErr, result.Err)
    }
    if result.Host != "unreachable.local" {
        t.Fatalf("unexpected host: %s", result.Host)
    }
}

func TestFormatResultQuiet(t *testing.T) {
    r := PingResult{Host: "example.com", Latency: 42 * time.Millisecond, Err: nil}
    out := formatResult(r, true)
    expected := "example.com,42"
    if out != expected {
        t.Fatalf("expected %s, got %s", expected, out)
    }
    rErr := PingResult{Host: "bad.host", Err: errors.New("boom")}
    outErr := formatResult(rErr, true)
    expectedErr := "bad.host,ERROR"
    if outErr != expectedErr {
        t.Fatalf("expected %s, got %s", expectedErr, outErr)
    }
}

func TestFormatResultVerbose(t *testing.T) {
    r := PingResult{Host: "example.com", Latency: 123 * time.Millisecond, Err: nil}
    out := formatResult(r, false)
    if !strings.Contains(out, "example.com responded in 123ms") {
        t.Fatalf("unexpected verbose output: %s", out)
    }
    rErr := PingResult{Host: "bad.host", Err: errors.New("boom")}
    outErr := formatResult(rErr, false)
    if !strings.Contains(outErr, "bad.host is unreachable") {
        t.Fatalf("unexpected verbose error output: %s", outErr)
    }
}
