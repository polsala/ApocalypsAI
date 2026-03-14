package main

import (
    "bytes"
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"
    "time"
)

func TestBottleService(t *testing.T) {
    // Create a store with a short retention window for deterministic testing.
    store := NewStore(2 * time.Minute)
    server := httptest.NewServer(NewHandler(store))
    defer server.Close()

    // POST a message.
    msg := map[string]string{"msg": "hello world"}
    body, _ := json.Marshal(msg)
    resp, err := http.Post(server.URL+"/bottle", "application/json", bytes.NewReader(body))
    if err != nil {
        t.Fatalf("POST request failed: %v", err)
    }
    if resp.StatusCode != http.StatusOK {
        t.Fatalf("expected 200 OK, got %d", resp.StatusCode)
    }
    resp.Body.Close()

    // GET messages and verify the posted one is present.
    resp, err = http.Get(server.URL + "/bottle")
    if err != nil {
        t.Fatalf("GET request failed: %v", err)
    }
    defer resp.Body.Close()
    var got []Message
    if err := json.NewDecoder(resp.Body).Decode(&got); err != nil {
        t.Fatalf("failed to decode response: %v", err)
    }
    if len(got) != 1 || got[0].Text != "hello world" {
        t.Fatalf("unexpected messages: %+v", got)
    }

    // Insert an old message directly into the store (beyond retention).
    oldMsg := Message{
        Text:      "old message",
        Timestamp: time.Now().Add(-5 * time.Minute).UTC(),
    }
    store.mu.Lock()
    store.msgs = append(store.msgs, oldMsg)
    store.mu.Unlock()

    // GET again; old message should be filtered out.
    resp, err = http.Get(server.URL + "/bottle")
    if err != nil {
        t.Fatalf("GET request failed: %v", err)
    }
    defer resp.Body.Close()
    var got2 []Message
    if err := json.NewDecoder(resp.Body).Decode(&got2); err != nil {
        t.Fatalf("failed to decode response: %v", err)
    }
    if len(got2) != 1 {
        t.Fatalf("expected only recent messages, got %d", len(got2))
    }
}
