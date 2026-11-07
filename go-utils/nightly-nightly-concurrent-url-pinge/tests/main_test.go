package main

import (
    "net/http"
    "net/http/httptest"
    "testing"
    "time"
)

// TestCheckURL_Up verifies that a healthy server is reported as UP.
func TestCheckURL_Up(t *testing.T) {
    // Mock server that returns 200 OK immediately.
    srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
    }))
    defer srv.Close()

    status := checkURL(srv.URL)
    if status != "UP" {
        t.Fatalf("expected UP, got %s", status)
    }
}

// TestCheckURL_Down verifies that a server that times out is reported as DOWN.
func TestCheckURL_Down(t *testing.T) {
    // Mock server that sleeps longer than the client timeout (5s).
    srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(6 * time.Second)
        w.WriteHeader(http.StatusOK)
    }))
    defer srv.Close()

    status := checkURL(srv.URL)
    if status != "DOWN" {
        t.Fatalf("expected DOWN due to timeout, got %s", status)
    }
}
