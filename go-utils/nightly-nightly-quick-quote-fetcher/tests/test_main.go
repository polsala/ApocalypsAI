package main

import (
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestFetchQuoteSuccess(t *testing.T) {
    handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        w.WriteHeader(http.StatusOK)
        w.Write([]byte(`{"content":"Test quote","author":"Tester"}`))
    })
    ts := httptest.NewServer(handler)
    defer ts.Close()

    q, err := fetchQuote(ts.URL)
    if err != nil {
        t.Fatalf("expected no error, got %v", err)
    }
    if q.Content != "Test quote" || q.Author != "Tester" {
        t.Fatalf("unexpected quote: %+v", q)
    }
}

func TestFetchQuoteNon200(t *testing.T) {
    handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusInternalServerError)
    })
    ts := httptest.NewServer(handler)
    defer ts.Close()

    _, err := fetchQuote(ts.URL)
    if err == nil {
        t.Fatalf("expected error, got nil")
    }
}
