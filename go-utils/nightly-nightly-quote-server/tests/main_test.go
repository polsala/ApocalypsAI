package main

import (
    "encoding/json"
    "math/rand"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestQuoteHandler_Deterministic(t *testing.T) {
    // Mock the quotes slice to a single known entry for predictability
    originalQuotes := quotes
    defer func() { quotes = originalQuotes }()
    quotes = []Quote{{"Test quote", "Tester"}}

    // Seed the random generator (not strictly needed with a single quote, but kept for completeness)
    rand.Seed(12345)

    // Use a zero TTL so the cache always fetches a new quote (which will be the mocked one)
    cache := NewQuoteCache(0)
    handler := quoteHandler(cache)

    req := httptest.NewRequest("GET", "/quote", nil)
    w := httptest.NewRecorder()
    handler(w, req)

    resp := w.Result()
    if resp.StatusCode != http.StatusOK {
        t.Fatalf("expected status 200, got %d", resp.StatusCode)
    }
    var q Quote
    if err := json.NewDecoder(resp.Body).Decode(&q); err != nil {
        t.Fatalf("failed to decode JSON response: %v", err)
    }
    expected := Quote{Text: "Test quote", Author: "Tester"}
    if q != expected {
        t.Fatalf("expected %+v, got %+v", expected, q)
    }
}
