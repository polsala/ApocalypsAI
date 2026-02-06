package main

import (
    "encoding/json"
    "math/rand"
    "net/http/httptest"
    "testing"
)

func TestEchoHandler(t *testing.T) {
    // Mock deterministic random by fixing seed so the chosen phrase is predictable.
    // # Mock rationale: we set a fixed seed so the chosen phrase is deterministic.
    rand.Seed(1)

    req := httptest.NewRequest(http.MethodGet, "/echo?msg=TestMessage", nil)
    w := httptest.NewRecorder()
    echoHandler(w, req)

    resp := w.Result()
    if resp.StatusCode != http.StatusOK {
        t.Fatalf("expected status 200, got %d", resp.StatusCode)
    }

    var r response
    if err := json.NewDecoder(resp.Body).Decode(&r); err != nil {
        t.Fatalf("failed to decode json: %v", err)
    }

    if r.Original != "TestMessage" {
        t.Errorf("expected original 'TestMessage', got %s", r.Original)
    }

    // With seed 1, rand.Intn(len(phrases)) yields 1 (checked)
    expected := phrases[1]
    if r.Doom != expected {
        t.Errorf("expected doom phrase %q, got %q", expected, r.Doom)
    }
}

func TestEchoHandlerMissingMsg(t *testing.T) {
    req := httptest.NewRequest(http.MethodGet, "/echo", nil)
    w := httptest.NewRecorder()
    echoHandler(w, req)

    if w.Code != http.StatusBadRequest {
        t.Fatalf("expected status 400, got %d", w.Code)
    }
}
