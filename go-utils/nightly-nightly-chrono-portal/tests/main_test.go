package main

import (
    "bytes"
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestConvertHandler_Success(t *testing.T) {
    // Mock request payload
    reqBody := ConvertRequest{
        Timestamp: "2023-10-10T12:00:00Z",
        Timezone:  "America/New_York",
    }
    payload, _ := json.Marshal(reqBody)
    req := httptest.NewRequest(http.MethodPost, "/convert", bytes.NewReader(payload))
    w := httptest.NewRecorder()

    convertHandler(w, req)

    resp := w.Result()
    if resp.StatusCode != http.StatusOK {
        t.Fatalf("expected status 200, got %d", resp.StatusCode)
    }
    var respBody ConvertResponse
    if err := json.NewDecoder(resp.Body).Decode(&respBody); err != nil {
        t.Fatalf("failed to decode response: %v", err)
    }
    // 2023-10-10 12:00:00 UTC -> 08:00:00 in New York (EDT, UTC‑4)
    expected := "The sands of time now read: 2023-10-10 08:00:00 (America/New_York)"
    if respBody.Message != expected {
        t.Fatalf("unexpected message: got %q, want %q", respBody.Message, expected)
    }
}

func TestConvertHandler_InvalidMethod(t *testing.T) {
    req := httptest.NewRequest(http.MethodGet, "/convert", nil)
    w := httptest.NewRecorder()
    convertHandler(w, req)
    if w.Result().StatusCode != http.StatusMethodNotAllowed {
        t.Fatalf("expected status 405, got %d", w.Result().StatusCode)
    }
}
