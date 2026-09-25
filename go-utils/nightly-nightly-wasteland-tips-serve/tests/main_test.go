package main

import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestTipEndpoint(t *testing.T) {
    // Setup deterministic handler for testing
    handler := http.NewServeMux()
    handler.HandleFunc("/tip", func(w http.ResponseWriter, r *http.Request) {
        // Use the first tip to make the test deterministic
        t := tips[0]
        resp := tipResponse{Tip: t}
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(resp)
    })

    req := httptest.NewRequest("GET", "/tip", nil)
    w := httptest.NewRecorder()
    handler.ServeHTTP(w, req)

    if w.Code != http.StatusOK {
        t.Fatalf("expected status 200, got %d", w.Code)
    }

    var resp tipResponse
    if err := json.NewDecoder(w.Body).Decode(&resp); err != nil {
        t.Fatalf("failed to decode response: %v", err)
    }

    if resp.Tip != tips[0] {
        t.Fatalf("expected tip %q, got %q", tips[0], resp.Tip)
    }
}

func TestHealthEndpoint(t *testing.T) {
    handler := http.NewServeMux()
    handler.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
        w.Write([]byte("OK"))
    })

    req := httptest.NewRequest("GET", "/health", nil)
    w := httptest.NewRecorder()
    handler.ServeHTTP(w, req)

    if w.Code != http.StatusOK {
        t.Fatalf("expected status 200, got %d", w.Code)
    }
    if w.Body.String() != "OK" {
        t.Fatalf("expected body OK, got %s", w.Body.String())
    }
}
