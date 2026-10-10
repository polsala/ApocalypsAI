package main

import (
    "fmt"
    "reflect"
    "testing"
    "time"
)

// mockPingFactory creates a PingFunc that returns predefined latencies or errors.
func mockPingFactory(latencies map[string]time.Duration, errs map[string]error) PingFunc {
    return func(host string) (time.Duration, error) {
        if err, ok := errs[host]; ok {
            return 0, err
        }
        if lat, ok := latencies[host]; ok {
            return lat, nil
        }
        return 0, nil
    }
}

func TestPingHosts(t *testing.T) {
    hosts := []string{"alpha", "beta", "gamma"}
    latMap := map[string]time.Duration{
        "alpha": 100 * time.Millisecond,
        "beta":  200 * time.Millisecond,
    }
    errMap := map[string]error{
        "gamma": fmt.Errorf("unreachable"),
    }
    pingFn := mockPingFactory(latMap, errMap)

    results := PingHosts(hosts, pingFn)

    expected := []PingResult{
        {Host: "alpha", Latency: 100 * time.Millisecond},
        {Host: "beta", Latency: 200 * time.Millisecond},
        {Host: "gamma", Error: "unreachable"},
    }

    if !reflect.DeepEqual(results, expected) {
        t.Fatalf("expected %+v, got %+v", expected, results)
    }
}
