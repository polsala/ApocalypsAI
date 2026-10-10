package main

import (
    "errors"
    "reflect"
    "testing"
    "time"
)

// mockDial simulates latency based on host name.
func mockDial(host string) (time.Duration, error) {
    switch host {
    case "fast.example":
        return 30 * time.Millisecond, nil
    case "slow.example":
        return 150 * time.Millisecond, nil
    case "error.example":
        return 0, errors.New("mock connection error")
    default:
        return 0, errors.New("unknown host")
    }
}

func TestPingHosts_Mocked(t *testing.T) {
    // Replace the global dialer with the mock.
    originalDialer := dialerFunc
    dialerFunc = mockDial
    defer func() { dialerFunc = originalDialer }()

    hosts := []string{"slow.example", "fast.example", "error.example"}
    results := pingHosts(hosts)

    // Expected order: fast, slow, error.
    expected := []pingResult{
        {Host: "fast.example", Latency: 30 * time.Millisecond, Err: nil},
        {Host: "slow.example", Latency: 150 * time.Millisecond, Err: nil},
        {Host: "error.example", Latency: 0, Err: errors.New("mock connection error")},
    }

    // Compare only Host and Err messages; Latency is checked for the first two entries.
    for i, exp := range expected {
        got := results[i]
        if got.Host != exp.Host {
            t.Fatalf("result %d host mismatch: got %s, want %s", i, got.Host, exp.Host)
        }
        if (got.Err == nil) != (exp.Err == nil) {
            t.Fatalf("result %d error presence mismatch: got %v, want %v", i, got.Err, exp.Err)
        }
        if got.Err != nil && exp.Err != nil && got.Err.Error() != exp.Err.Error() {
            t.Fatalf("result %d error message mismatch: got %s, want %s", i, got.Err.Error(), exp.Err.Error())
        }
        if got.Err == nil && got.Latency != exp.Latency {
            t.Fatalf("result %d latency mismatch: got %v, want %v", i, got.Latency, exp.Latency)
        }
    }

    // Ensure the slice length matches.
    if len(results) != len(expected) {
        t.Fatalf("unexpected number of results: got %d, want %d", len(results), len(expected))
    }

    // Verify sorting stability for errors (alphabetical order if multiple errors).
    // Add a second error host to test.
    hosts = []string{"error.example", "unknown.example"}
    results = pingHosts(hosts)
    if !reflect.DeepEqual([]string{results[0].Host, results[1].Host}, []string{"error.example", "unknown.example"}) {
        t.Fatalf("error hosts not sorted alphabetically: %v", results)
    }
}
