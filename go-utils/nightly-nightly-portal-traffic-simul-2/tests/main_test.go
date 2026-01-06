package main

import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "sync/atomic"
    "testing"
    "time"
)

func TestMetricsHandler(t *testing.T) {
    // reset stats
    atomic.StoreUint64(&stats.Total, 0)
    atomic.StoreUint64(&stats.Active, 0)

    // simulate deterministic travelers
    go func() {
        for i := 0; i < 5; i++ {
            traveler(10 * time.Millisecond)
        }
    }()

    // give goroutine time to finish
    time.Sleep(50 * time.Millisecond)

    req := httptest.NewRequest("GET", "/metrics", nil)
    w := httptest.NewRecorder()
    metricsHandler(w, req)

    resp := w.Result()
    if resp.StatusCode != http.StatusOK {
        t.Fatalf("expected status 200, got %d", resp.StatusCode)
    }

    var got Stats
    if err := json.NewDecoder(resp.Body).Decode(&got); err != nil {
        t.Fatalf("failed to decode json: %v", err)
    }

    if got.Total != 5 {
        t.Errorf("expected total 5, got %d", got.Total)
    }
    if got.Active != 0 {
        t.Errorf("expected active 0, got %d", got.Active)
    }
}
