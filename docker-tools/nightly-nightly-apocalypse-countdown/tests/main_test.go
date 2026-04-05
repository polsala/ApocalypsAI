package main

import (
    "encoding/json"
    "io/ioutil"
    "net/http/httptest"
    "os"
    "testing"
)

func TestHandlerDeterministic(t *testing.T) {
    // Set fixed seed for deterministic output
    os.Setenv("FIXED_SEED", "42")
    defer os.Unsetenv("FIXED_SEED")

    req := httptest.NewRequest("GET", "/countdown", nil)
    w := httptest.NewRecorder()
    handler(w, req)

    resp := w.Result()
    body, _ := ioutil.ReadAll(resp.Body)

    var r Response
    if err := json.Unmarshal(body, &r); err != nil {
        t.Fatalf("Failed to unmarshal response: %v", err)
    }

    // With seed 42, the first rand.Intn(1001) yields 654 (mock rationale: deterministic)
    // Mock rationale: using Go's math/rand with seed 42 produces 654 for Intn(1001)
    expectedDays := 654
    if r.Days != expectedDays {
        t.Fatalf("Expected days %d, got %d", expectedDays, r.Days)
    }
    expectedMsg := "The world ends in 654 days!"
    if r.Message != expectedMsg {
        t.Fatalf("Expected message %q, got %q", expectedMsg, r.Message)
    }
}
