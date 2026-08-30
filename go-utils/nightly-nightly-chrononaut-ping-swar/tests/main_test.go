package main

import (
    "errors"
    "reflect"
    "testing"
    "time"
)

// mockPingFactory returns a function that yields predefined latencies or errors for given hosts.
func mockPingFactory(res map[string]struct{lat time.Duration; err error}) func(string) (time.Duration, error) {
    return func(host string) (time.Duration, error) {
        if r, ok := res[host]; ok {
            return r.lat, r.err
        }
        return 0, errors.New("unknown host")
    }
}

func TestRunPingSwarm_SortedResults(t *testing.T) {
    // Mock responses: alpha fast, beta slower, gamma error.
    mockResponses := map[string]struct{lat time.Duration; err error}{
        "alpha": {lat: 50 * time.Millisecond, err: nil},
        "beta":  {lat: 120 * time.Millisecond, err: nil},
        "gamma": {lat: 0, err: errors.New("dial timeout")},
    }
    // Replace the global pingFunc with our mock.
    pingFunc = mockPingFactory(mockResponses)
    defer func() { pingFunc = realPing }() // restore after test

    hosts := []string{"beta", "gamma", "alpha"}
    results, err := RunPingSwarm(hosts)
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    // Expected order: alpha (fastest), beta, gamma (error at end).
    expectedOrder := []string{"alpha", "beta", "gamma"}
    gotOrder := []string{results[0].Host, results[1].Host, results[2].Host}
    if !reflect.DeepEqual(expectedOrder, gotOrder) {
        t.Fatalf("expected order %v, got %v", expectedOrder, gotOrder)
    }
    // Verify error handling for gamma.
    if results[2].Err == nil {
        t.Fatalf("expected error for host gamma, got nil")
    }
}
