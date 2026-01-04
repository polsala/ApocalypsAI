package main

import (
    "bytes"
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "sync"
    "testing"
)

func TestEchoHandler(t *testing.T) {
    handler := NewHandler()
    server := httptest.NewServer(handler)
    defer server.Close()

    payload := []byte(`{"msg":"hello"}`)
    resp, err := http.Post(server.URL+"/echo", "application/json", bytes.NewReader(payload))
    if err != nil {
        t.Fatalf("POST request failed: %v", err)
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        t.Fatalf("expected status 200, got %d", resp.StatusCode)
    }

    var result EchoResponse
    if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
        t.Fatalf("failed to decode response: %v", err)
    }

    if result.Echo != string(payload) {
        t.Errorf("expected echo %q, got %q", string(payload), result.Echo)
    }
    if result.Lantern != "🏮" {
        t.Errorf("expected lantern emoji, got %q", result.Lantern)
    }
}

func TestConcurrentRequests(t *testing.T) {
    handler := NewHandler()
    server := httptest.NewServer(handler)
    defer server.Close()

    var wg sync.WaitGroup
    const concurrent = 10
    for i := 0; i < concurrent; i++ {
        wg.Add(1)
        go func(i int) {
            defer wg.Done()
            payload := []byte(`{"msg":"msg` + string(i+'0') + `"}`)
            resp, err := http.Post(server.URL+"/echo", "application/json", bytes.NewReader(payload))
            if err != nil {
                t.Errorf("goroutine %d POST failed: %v", i, err)
                return
            }
            defer resp.Body.Close()
            var result EchoResponse
            if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
                t.Errorf("goroutine %d decode failed: %v", i, err)
                return
            }
            if result.Echo != string(payload) {
                t.Errorf("goroutine %d expected echo %q, got %q", i, string(payload), result.Echo)
            }
        }(i)
    }
    wg.Wait()
}
