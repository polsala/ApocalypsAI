package main

import (
    "math/rand"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestQuoteHandler(t *testing.T) {
    // Ensure deterministic output by resetting the random seed
    rand.Seed(1) // # Mock rationale: deterministic seed ensures this exact output
    req := httptest.NewRequest("GET", "/quote", nil)
    w := httptest.NewRecorder()
    quoteHandler(w, req)
    resp := w.Result()
    if resp.StatusCode != http.StatusOK {
        t.Fatalf("expected status 200, got %d", resp.StatusCode)
    }
    expected := "{\"quote\":\"Reach for the stars — as the world crumbles\"}"
    if w.Body.String() != expected {
        t.Fatalf("expected body %s, got %s", expected, w.Body.String())
    }
}
