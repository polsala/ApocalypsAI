package main

import (
    "errors"
    "net"
    "testing"
    "time"
)

// mockDialer returns a fake connection after a predetermined delay based on the host name.
func mockDialer(network, address string, timeout time.Duration) (net.Conn, error) {
    // Extract host part (address is host:port).
    host, _, err := net.SplitHostPort(address)
    if err != nil {
        return nil, err
    }
    // Define artificial latencies.
    switch host {
    case "fast.example.com":
        time.Sleep(10 * time.Millisecond)
        return &net.TCPConn{}, nil // dummy non‑nil conn
    case "slow.example.com":
        time.Sleep(100 * time.Millisecond)
        return &net.TCPConn{}, nil
    case "unreachable.example.com":
        return nil, errors.New("dial timeout")
    default:
        // For any other host, simulate a quick success.
        time.Sleep(5 * time.Millisecond)
        return &net.TCPConn{}, nil
    }
}

func TestPingHostSuccess(t *testing.T) {
    latency, err := pingHost("fast.example.com", 1*time.Second, mockDialer)
    if err != nil {
        t.Fatalf("expected no error, got %v", err)
    }
    if latency < 10 || latency > 30 {
        t.Fatalf("expected latency around 10ms, got %dms", latency)
    }
}

func TestPingHostError(t *testing.T) {
    _, err := pingHost("unreachable.example.com", 1*time.Second, mockDialer)
    if err == nil {
        t.Fatalf("expected an error for unreachable host")
    }
    if err.Error() != "dial timeout" {
        t.Fatalf("unexpected error message: %v", err)
    }
}

func TestConcurrentPing(t *testing.T) {
    hosts := []string{"fast.example.com", "slow.example.com", "unreachable.example.com"}
    results := concurrentPing(hosts, 2*time.Second, mockDialer)

    if len(results) != len(hosts) {
        t.Fatalf("expected %d results, got %d", len(hosts), len(results))
    }

    // fast host
    if r, ok := results["fast.example.com"]; !ok || r.Error != "" {
        t.Fatalf("fast host should succeed, got %+v", r)
    } else if r.LatencyMs < 10 || r.LatencyMs > 30 {
        t.Fatalf("fast host latency out of expected range: %dms", r.LatencyMs)
    }

    // slow host
    if r, ok := results["slow.example.com"]; !ok || r.Error != "" {
        t.Fatalf("slow host should succeed, got %+v", r)
    } else if r.LatencyMs < 90 || r.LatencyMs > 130 {
        t.Fatalf("slow host latency out of expected range: %dms", r.LatencyMs)
    }

    // unreachable host
    if r, ok := results["unreachable.example.com"]; !ok || r.Error != "dial timeout" {
        t.Fatalf("unreachable host should report error, got %+v", r)
    }
}
