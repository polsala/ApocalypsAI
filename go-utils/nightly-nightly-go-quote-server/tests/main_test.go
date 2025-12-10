package main

import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestQuoteHandler_Deterministic(t *testing.T) {
    // Mock request with a known seed
    req := httptest.NewRequest(http.MethodGet, "/quote?seed=42", nil)
    w := httptest.NewRecorder()
    quoteHandler(w, req)

    res := w.Result()
    defer res.Body.Close()

    if res.StatusCode != http.StatusOK {
        t.Fatalf("expected status 200, got %d", res.StatusCode)
    }
    var qr quoteResponse
    if err := json.NewDecoder(res.Body).Decode(&qr); err != nil {
        t.Fatalf("failed to decode JSON: %v", err)
    }
    // With seed=42 the expected index is deterministic (seed % len(quotes))
    // # Mock rationale: using the same algorithm as in handler, the first index will be 7
    expected := quotes[7]
    if qr.Quote != expected {
        t.Fatalf("expected quote %q, got %q", expected, qr.Quote)
    }
}

func TestQuoteHandler_NoSeed(t *testing.T) {
    // Ensure handler works without a seed and returns a valid JSON quote
    req := httptest.NewRequest(http.MethodGet, "/quote", nil)
    w := httptest.NewRecorder()
    quoteHandler(w, req)

    res := w.Result()
    defer res.Body.Close()

    if res.StatusCode != http.StatusOK {
        t.Fatalf("expected status 200, got %d", res.StatusCode)
    }
    var qr quoteResponse
    if err := json.NewDecoder(res.Body).Decode(&qr); err != nil {
        t.Fatalf("failed to decode JSON: %v", err)
    }
    if qr.Quote == "" {
        t.Fatalf("quote should not be empty")
    }
    // Verify the quote is one of the known list
    found := false
    for _, q := range quotes {
        if q == qr.Quote {
            found = true
            break
        }
    }
    if !found {
        t.Fatalf("quote %q not found in known list", qr.Quote)
    }
}
