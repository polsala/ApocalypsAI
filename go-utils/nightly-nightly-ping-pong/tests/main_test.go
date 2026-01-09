package main

import (
    "net/http"
    "net/http/httptest"
    "strings"
    "testing"
    "time"
)

// Mock rationale: We spin up two local HTTP servers that deliberately delay their response.
// This allows us to test pingHosts without external network dependencies.
func TestPingHosts(t *testing.T) {
    // Server that responds quickly (≈10ms)
    fastSrv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(10 * time.Millisecond)
        w.WriteHeader(http.StatusOK)
    }))
    defer fastSrv.Close()

    // Server that responds slowly (≈200ms)
    slowSrv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(200 * time.Millisecond)
        w.WriteHeader(http.StatusOK)
    }))
    defer slowSrv.Close()

    // Extract host:port without scheme
    fastHost := strings.TrimPrefix(fastSrv.URL, "http://")
    slowHost := strings.TrimPrefix(slowSrv.URL, "http://")

    hosts := []string{fastHost, slowHost}
    timeout := 1 * time.Second
    results := pingHosts(hosts, timeout)

    // Verify fast host latency is within expected range
    if dur, ok := results[fastHost]; !ok || dur <= 0 || dur > 50*time.Millisecond {
        t.Fatalf("expected fast host latency <50ms, got %v", dur)
    }

    // Verify slow host latency is within expected range
    if dur, ok := results[slowHost]; !ok || dur < 150*time.Millisecond || dur > 300*time.Millisecond {
        t.Fatalf("expected slow host latency ~200ms, got %v", dur)
    }
}
