package main

import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestQuoteHandler(t *testing.T) {
    req := httptest.NewRequest(http.MethodGet, "/quote", nil)
    w := httptest.NewRecorder()
    quoteHandler(w, req)

    resp := w.Result()
    if resp.StatusCode != http.StatusOK {
        t.Fatalf("expected status 200, got %d", resp.StatusCode)
    }
    var qr QuoteResponse
    if err := json.NewDecoder(resp.Body).Decode(&qr); err != nil {
        t.Fatalf("failed to decode json: %v", err)
    }
    // Verify the quote is one of the known quotes
    found := false
    for _, q := range quotes {
        if q == qr.Quote {
            found = true
            break
        }
    }
    if !found {
        t.Fatalf("unexpected quote: %s", qr.Quote)
    }
}
