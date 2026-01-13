package main

import (
    "encoding/json"
    "math/rand"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestMixQuoteDeterministic(t *testing.T) {
    // Use a fixed seed to make the output predictable
    rng = rand.New(rand.NewSource(1))
    // Replicate the selection logic to compute the expected result
    i := rng.Intn(len(inspirational))
    a := rng.Intn(len(apocalyptic))
    expected := inspirational[i] + " " + apocalyptic[a] + "."

    // Reset rng for the function under test
    rng = rand.New(rand.NewSource(1))
    got := mixQuote()
    if got != expected {
        t.Fatalf(\"expected %q, got %q\", expected, got)
    }
}

func TestQuoteHandlerDeterministic(t *testing.T) {
    // Fixed seed ensures the same quote each run
    rng = rand.New(rand.NewSource(2))
    // Build the expected response using the same seed
    i := rng.Intn(len(inspirational))
    a := rng.Intn(len(apocalyptic))
    expectedQuote := inspirational[i] + " " + apocalyptic[a] + "."

    // Reset rng for the handler
    rng = rand.New(rand.NewSource(2))
    req := httptest.NewRequest(http.MethodGet, \"/quote\", nil)
    w := httptest.NewRecorder()
    quoteHandler(w, req)

    if w.Code != http.StatusOK {
        t.Fatalf(\"expected status 200, got %d\", w.Code)
    }
    var resp QuoteResponse
    if err := json.NewDecoder(w.Body).Decode(&resp); err != nil {
        t.Fatalf(\"failed to decode JSON response: %v\", err)
    }
    if resp.Quote != expectedQuote {
        t.Fatalf(\"expected quote %q, got %q\", expectedQuote, resp.Quote)
    }
}

