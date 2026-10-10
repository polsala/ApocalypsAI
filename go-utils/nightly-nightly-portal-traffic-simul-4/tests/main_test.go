package main

import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "sync/atomic"
    "testing"
    "math/rand"
)

func TestGreetHandler(t *testing.T) {
    // # Mock rationale: set a deterministic random seed before invoking the handler
    rand.Seed(1)
    req := httptest.NewRequest(http.MethodGet, "/greet", nil)
    w := httptest.NewRecorder()
    greetHandler(w, req)

    if w.Code != http.StatusOK {
        t.Fatalf("expected status 200, got %d", w.Code)
    }
    var resp map[string]string
    if err := json.NewDecoder(w.Body).Decode(&resp); err != nil {
        t.Fatalf("failed to decode response: %v", err)
    }
    // With seed 1, the first rand.Intn yields index 0 for our slice
    expected := messages[0]
    if resp["message"] != expected {
        t.Fatalf("expected message %q, got %q", expected, resp["message"])
    }
}

func TestStatsHandler(t *testing.T) {
    // Reset the global counter
    atomic.StoreUint64(&requestCount, 0)
    // Simulate two greet requests
    for i := 0; i < 2; i++ {
        req := httptest.NewRequest(http.MethodGet, "/greet", nil)
        w := httptest.NewRecorder()
        greetHandler(w, req)
    }
    // Now query stats
    req := httptest.NewRequest(http.MethodGet, "/stats", nil)
    w := httptest.NewRecorder()
    statsHandler(w, req)

    if w.Code != http.StatusOK {
        t.Fatalf("expected status 200, got %d", w.Code)
    }
    var resp map[string]uint64
    if err := json.NewDecoder(w.Body).Decode(&resp); err != nil {
        t.Fatalf("failed to decode response: %v", err)
    }
    if resp["total_requests"] != 2 {
        t.Fatalf("expected total_requests 2, got %d", resp["total_requests"])
    }
}
