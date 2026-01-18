package main

import (
    "encoding/json"
    "math/rand"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestTipHandler(t *testing.T) {
    // deterministic random seed for reproducibility
    rand.Seed(1)
    req := httptest.NewRequest(http.MethodGet, "/tip", nil)
    w := httptest.NewRecorder()
    tipHandler(w, req)

    resp := w.Result()
    if resp.StatusCode != http.StatusOK {
        t.Fatalf("expected status 200, got %d", resp.StatusCode)
    }
    var tr tipResponse
    if err := json.NewDecoder(resp.Body).Decode(&tr); err != nil {
        t.Fatalf("failed to decode json: %v", err)
    }
    // verify the tip is one of the predefined tips
    found := false
    for _, tip := range tips {
        if tip == tr.Tip {
            found = true
            break
        }
    }
    if !found {
        t.Fatalf("unexpected tip: %s", tr.Tip)
    }
}
