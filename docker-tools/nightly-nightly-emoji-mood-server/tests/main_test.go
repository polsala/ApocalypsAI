package main

import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestEmojiHandler(t *testing.T) {
    req := httptest.NewRequest(http.MethodGet, "/emoji?mood=happy", nil)
    w := httptest.NewRecorder()
    emojiHandler(w, req)

    resp := w.Result()
    if resp.StatusCode != http.StatusOK {
        t.Fatalf("expected status 200, got %d", resp.StatusCode)
    }

    var data map[string]string
    if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
        t.Fatalf("failed to decode json: %v", err)
    }

    expected := "😊"
    if data["emoji"] != expected {
        t.Fatalf("expected emoji %s, got %s", expected, data["emoji"])
    }
}
