package main

import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestTeleportHandler(t *testing.T) {
    req := httptest.NewRequest("GET", "/teleport?time=2023-01-01T15:04:05Z&tz=UTC", nil)
    w := httptest.NewRecorder()
    teleportHandler(w, req)

    if w.Code != http.StatusOK {
        t.Fatalf("expected status 200, got %d", w.Code)
    }

    var resp response
    err := json.NewDecoder(w.Body).Decode(&resp)
    if err != nil {
        t.Fatalf("failed to decode response: %v", err)
    }

    expectedOriginal := "2023-01-01T15:04:05Z"
    if resp.Original != expectedOriginal {
        t.Errorf("original mismatch: got %s, want %s", resp.Original, expectedOriginal)
    }

    expectedTarget := "2023-01-01T15:04:05Z"
    if resp.Target != expectedTarget {
        t.Errorf("target mismatch: got %s, want %s", resp.Target, expectedTarget)
    }

    // Deterministic message based on tz "UTC"
    expectedMessage := getMessage("UTC")
    if resp.Message != expectedMessage {
        t.Errorf("message mismatch: got %s, want %s", resp.Message, expectedMessage)
    }
}
