package main

import (
    "errors"
    "testing"
    "time"
)

func mockPingFactory(delays map[string]time.Duration, errs map[string]error) func(string) PingResult {
    return func(host string) PingResult {
        d := delays[host]
        e := errs[host]
        return PingResult{Host: host, Latency: d, Err: e}
    }
}

func TestPingHostsConcurrently(t *testing.T) {
    hosts := []string{"alpha", "beta", "gamma"}
    delays := map[string]time.Duration{
        "alpha": 10 * time.Millisecond,
        "beta":  20 * time.Millisecond,
        "gamma": 0,
    }
    errs := map[string]error{
        "gamma": errors.New("unreachable"),
    }
    pingFunc := mockPingFactory(delays, errs)
    results := pingHostsConcurrently(hosts, pingFunc)

    if len(results) != len(hosts) {
        t.Fatalf("expected %d results, got %d", len(hosts), len(results))
    }
    for _, r := range results {
        expectedDelay := delays[r.Host]
        expectedErr := errs[r.Host]
        if r.Latency != expectedDelay {
            t.Errorf("host %s latency: expected %v, got %v", r.Host, expectedDelay, r.Latency)
        }
        if (r.Err == nil) != (expectedErr == nil) {
            t.Errorf("host %s error mismatch: expected %v, got %v", r.Host, expectedErr, r.Err)
        } else if r.Err != nil && r.Err.Error() != expectedErr.Error() {
            t.Errorf("host %s error text mismatch: expected %s, got %s", r.Host, expectedErr.Error(), r.Err.Error())
        }
    }
}
