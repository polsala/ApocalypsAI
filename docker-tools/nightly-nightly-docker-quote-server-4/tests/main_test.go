package main

import (
    "encoding/json"
    "math/rand"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestGetRandomQuoteDeterministic(t *testing.T) {
    rand.Seed(1) // fixed seed for deterministic output
    q := getRandomQuote()
    // Ensure the quote is one of the predefined list
    found := false
    for _, v := range quotes {
        if v == q {
            found = true
            break
        }
    }
    if !found {
        t.Fatalf("Quote not in list: %s", q)
    }
}

func TestQuoteHandler(t *testing.T) {
    rand.Seed(42) // deterministic seed for reproducibility
    req := httptest.NewRequest(http.MethodGet, "/", nil)
    w := httptest.NewRecorder()
    quoteHandler(w, req)

    resp := w.Result()
    if resp.StatusCode != http.StatusOK {
        t.Fatalf("expected status 200, got %d", resp.StatusCode)
    }
    var qr quoteResponse
    if err := json.NewDecoder(resp.Body).Decode(&qr); err != nil {
        t.Fatalf("failed to decode json: %v", err)
    }
    // Verify the returned quote is from the list
    found := false
    for _, v := range quotes {
        if v == qr.Quote {
            found = true
            break
        }
    }
    if !found {
        t.Fatalf("response quote not in list: %s", qr.Quote)
    }
}
