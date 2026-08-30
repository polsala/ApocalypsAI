package main

import (
    "io/ioutil"
    "net/http"
    "net/http/httptest"
    "testing"
)

// mockSensor implements the Sensor interface for testing.
type mockSensor struct {
    level int
}

func (m *mockSensor) GetLevel() int {
    return m.level
}

func TestRadiationHandler(t *testing.T) {
    // Inject a mock sensor that always returns 42.
    sensor = &mockSensor{level: 42}

    req := httptest.NewRequest("GET", "/radiation", nil)
    w := httptest.NewRecorder()
    radiationHandler(w, req)

    resp := w.Result()
    body, _ := ioutil.ReadAll(resp.Body)

    // Expected JSON output (the encoder adds a newline).
    expected := "{\"level\":42}\n"
    if string(body) != expected {
        t.Fatalf("expected %s, got %s", expected, string(body))
    }
    if ct := resp.Header.Get("Content-Type"); ct != "application/json" {
        t.Fatalf("expected Content-Type application/json, got %s", ct)
    }
}
