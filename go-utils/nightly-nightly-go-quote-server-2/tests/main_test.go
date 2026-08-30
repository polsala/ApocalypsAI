package main

import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "strings"
    "testing"
)

func TestHealthEndpoint(t *testing.T) {
    server := httptest.NewServer(NewServer([]string{}))
    defer server.Close()

    resp, err := http.Get(server.URL + "/health")
    if err != nil {
        t.Fatalf("Health request failed: %v", err)
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        t.Fatalf("Expected 200 OK, got %d", resp.StatusCode)
    }
    buf := new(strings.Builder)
    _, _ = buf.ReadFrom(resp.Body)
    if strings.TrimSpace(buf.String()) != "OK" {
        t.Fatalf("Expected body 'OK', got %q", buf.String())
    }
}

func TestQuoteEndpointReturnsOneOfProvidedQuotes(t *testing.T) {
    quotes := []string{"Quote A", "Quote B", "Quote C"}
    server := httptest.NewServer(NewServer(quotes))
    defer server.Close()

    resp, err := http.Get(server.URL + "/quote")
    if err != nil {
        t.Fatalf("Quote request failed: %v", err)
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        t.Fatalf("Expected 200 OK, got %d", resp.StatusCode)
    }
    var payload map[string]string
    if err := json.NewDecoder(resp.Body).Decode(&payload); err != nil {
        t.Fatalf("Failed to decode JSON: %v", err)
    }
    quote, ok := payload["quote"]
    if !ok {
        t.Fatalf("Response missing 'quote' field")
    }
    found := false
    for _, q := range quotes {
        if q == quote {
            found = true
            break
        }
    }
    if !found {
        t.Fatalf("Returned quote %q not in original list", quote)
    }
}
