package main

import (
    "io/ioutil"
    "math/rand"
    "net/http/httptest"
    "strings"
    "testing"
)

func TestQuoteHandler(t *testing.T) {
    // # Mock rationale: deterministic seed for reproducible output
    rand.Seed(1)
    req := httptest.NewRequest("GET", "/", nil)
    w := httptest.NewRecorder()
    quoteHandler(w, req)

    resp := w.Result()
    body, _ := ioutil.ReadAll(resp.Body)
    got := strings.TrimSpace(string(body))

    expected := quotes[1] // deterministic with seed 1
    if got != expected {
        t.Fatalf("expected %q, got %q", expected, got)
    }
}
