package main

import (
    "errors"
    "testing"
    "time"
)

// mockPinger returns predefined latencies or errors based on the host string.
func mockPingerFactory(latencies map[string]time.Duration, errHosts map[string]error) Pinger {
    return func(host string, timeout time.Duration) (time.Duration, error) {
        if err, ok := errHosts[host]; ok {
            return 0, err
        }
        if lat, ok := latencies[host]; ok {
            // Simulate work without actually sleeping.
            return lat, nil
        }
        return 0, errors.New("unknown host")
    }
}

func TestPingHostSuccess(t *testing.T) {
    latMap := map[string]time.Duration{"example.com:80": 25 * time.Millisecond}
    p := mockPingerFactory(latMap, nil)
    res := pingHost("example.com:80", 1*time.Second, p)
    if res.Err != nil {
        t.Fatalf("expected no error, got %v", res.Err)
    }
    if res.Latency != 25*time.Millisecond {
        t.Fatalf("expected 25ms latency, got %v", res.Latency)
    }
}

func TestPingHostTimeout(t *testing.T) {
    errMap := map[string]error{"10.0.0.1:22": errors.New("i/o timeout")}
    p := mockPingerFactory(nil, errMap)
    res := pingHost("10.0.0.1:22", 500*time.Millisecond, p)
    if res.Err == nil {
        t.Fatalf("expected timeout error, got nil")
    }
    if !errors.Is(res.Err, errMap["10.0.0.1:22"]) {
        t.Fatalf("expected specific timeout error, got %v", res.Err)
    }
}

func TestResultSorting(t *testing.T) {
    // Prepare a slice of results with mixed successes and failures.
    results := []PingResult{
        {Host: "a:1", Latency: 50 * time.Millisecond, Err: nil},
        {Host: "b:2", Latency: 0, Err: errors.New("timeout")},
        {Host: "c:3", Latency: 20 * time.Millisecond, Err: nil},
    }
    // Expected order: c (20ms), a (50ms), b (error)
    sort.Slice(results, func(i, j int) bool {
        if results[i].Err != nil && results[j].Err == nil {
            return false
        }
        if results[i].Err == nil && results[j].Err != nil {
            return true
        }
        return results[i].Latency < results[j].Latency
    })
    if results[0].Host != "c:3" || results[1].Host != "a:1" || results[2].Host != "b:2" {
        t.Fatalf("sorting failed, got order %v", []string{results[0].Host, results[1].Host, results[2].Host})
    }
}
