package main

import (
    "encoding/json"
    "net/http/httptest"
    "testing"
)

func TestHandlerDeterministic(t *testing.T) {
    seed := int64(12345)

    // First request with the seed
    req1 := httptest.NewRequest("GET", "/chatter?seed=12345", nil)
    w1 := httptest.NewRecorder()
    handler(w1, req1)
    var r1 Response
    if err := json.NewDecoder(w1.Result().Body).Decode(&r1); err != nil {
        t.Fatalf("failed to decode first response: %v", err)
    }

    // Second request with the same seed
    req2 := httptest.NewRequest("GET", "/chatter?seed=12345", nil)
    w2 := httptest.NewRecorder()
    handler(w2, req2)
    var r2 Response
    if err := json.NewDecoder(w2.Result().Body).Decode(&r2); err != nil {
        t.Fatalf("failed to decode second response: %v", err)
    }

    // # Mock rationale: With identical seeds the random generator should produce identical messages.
    if r1.Message != r2.Message {
        t.Fatalf("messages differ for same seed: %q vs %q", r1.Message, r2.Message)
    }
    if r1.Seed != seed || r2.Seed != seed {
        t.Fatalf("seed mismatch: got %d and %d, expected %d", r1.Seed, r2.Seed, seed)
    }
}
