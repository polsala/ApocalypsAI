package main

import (
    "net/http"
    "net/http/httptest"
    "reflect"
    "testing"
)

func TestFetchStatuses(t *testing.T) {
    // Mock server that returns 200 OK
    server200 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
    }))
    defer server200.Close()

    // Mock server that returns 404 Not Found
    server404 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusNotFound)
    }))
    defer server404.Close()

    urls := []string{server200.URL, server404.URL}
    got := fetchStatuses(urls)

    want := map[string]int{
        server200.URL: http.StatusOK,
        server404.URL: http.StatusNotFound,
    }

    if !reflect.DeepEqual(got, want) {
        t.Fatalf("fetchStatuses = %v, want %v", got, want)
    }
}
