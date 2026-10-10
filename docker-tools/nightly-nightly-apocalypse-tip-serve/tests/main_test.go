package main

import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestTipHandler_Deterministic(t *testing.T) {
    // Use a fixed seed to make the output predictable
    req := httptest.NewRequest(http.MethodGet, "/tip?seed=42", nil)
    w := httptest.NewRecorder()
    tipHandler(w, req)

    res := w.Result()
    if res.StatusCode != http.StatusOK {
        t.Fatalf("expected status 200, got %d", res.StatusCode)
    }
    var tr tipResponse
    if err := json.NewDecoder(res.Body).Decode(&tr); err != nil {
        t.Fatalf("failed to decode JSON: %v", err)
    }
    // With seed=42 the expected tip is known (pre‑computed)
    expected := "Never trust a stranger with a shiny object."
    if tr.Tip != expected {
        t.Fatalf("expected tip %q, got %q", expected, tr.Tip)
    }
}

func TestTipHandler_Random(t *testing.T) {
    // No seed – just ensure we get a valid tip from the list
    req := httptest.NewRequest(http.MethodGet, "/tip", nil)
    w := httptest.NewRecorder()
    tipHandler(w, req)
    res := w.Result()
    if res.StatusCode != http.StatusOK {
        t.Fatalf("expected status 200, got %d", res.StatusCode)
    }
    var tr tipResponse
    if err := json.NewDecoder(res.Body).Decode(&tr); err != nil {
        t.Fatalf("failed to decode JSON: %v", err)
    }
    // Verify the tip is one of the known entries
    found := false
    for _, t := range tips {
        if tr.Tip == t {
            found = true
            break
        }
    }
    if !found {
        t.Fatalf("returned tip not in known list: %q", tr.Tip)
    }
}
