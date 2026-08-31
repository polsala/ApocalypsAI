package main

import (
    "bytes"
    "encoding/json"
    "io/ioutil"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestQRHandlerSuccess(t *testing.T) {
    payload := map[string]string{"message": "test"}
    body, _ := json.Marshal(payload)
    req := httptest.NewRequest(http.MethodPost, "/qr", bytes.NewReader(body))
    w := httptest.NewRecorder()
    qrHandler(w, req)

    resp := w.Result()
    if resp.StatusCode != http.StatusOK {
        t.Fatalf("expected 200, got %d", resp.StatusCode)
    }
    if ct := resp.Header.Get("Content-Type"); ct != "image/png" {
        t.Fatalf("expected image/png content type, got %s", ct)
    }
    data, _ := ioutil.ReadAll(resp.Body)
    if len(data) == 0 {
        t.Fatalf("expected non-empty PNG data")
    }
    // PNG signature check
    if !bytes.HasPrefix(data, []byte{0x89, 0x50, 0x4e, 0x47}) {
        t.Fatalf("response does not start with PNG signature")
    }
}

func TestQRHandlerBadMethod(t *testing.T) {
    req := httptest.NewRequest(http.MethodGet, "/qr", nil)
    w := httptest.NewRecorder()
    qrHandler(w, req)
    if w.Code != http.StatusMethodNotAllowed {
        t.Fatalf("expected 405, got %d", w.Code)
    }
}

func TestQRHandlerInvalidJSON(t *testing.T) {
    req := httptest.NewRequest(http.MethodPost, "/qr", bytes.NewReader([]byte("{invalid")))
    w := httptest.NewRecorder()
    qrHandler(w, req)
    if w.Code != http.StatusBadRequest {
        t.Fatalf("expected 400, got %d", w.Code)
    }
}
