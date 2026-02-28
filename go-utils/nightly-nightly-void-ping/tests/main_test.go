package main

import (
    "net/http"
    "net/http/httptest"
    "testing"
    "time"
)

func TestCheckURLSuccess(t *testing.T) {
    // Mock server that returns 200 OK immediately.
    srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
    }))
    defer srv.Close()

    result := checkURL(srv.URL, 2*time.Second)
    expected := "✅ " + srv.URL + " responded with 200 OK"
    if !strings.Contains(result, expected) {
        t.Fatalf("expected result to contain %q, got %q", expected, result)
    }
}

func TestCheckURLTimeout(t *testing.T) {
    // Mock server that sleeps longer than the timeout.
    srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(3 * time.Second)
        w.WriteHeader(http.StatusOK)
    }))
    defer srv.Close()

    // Use a short timeout to trigger the timeout path.
    result := checkURL(srv.URL, 1*time.Second)
    expected := "☢️ " + srv.URL + " timed out after 1s"
    if !strings.Contains(result, expected) {
        t.Fatalf("expected timeout result %q, got %q", expected, result)
    }
}
