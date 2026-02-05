package main

import (
    "net/http"
    "net/http/httptest"
    "testing"
    "time"
)

func TestPingSuccess(t *testing.T) {
    // Mock server that responds instantly with 200 OK
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
    }))
    defer server.Close()

    result := ping(server.URL, 2*time.Second)
    if !result.Success {
        t.Fatalf("expected success, got error: %s", result.Error)
    }
    if result.Latency <= 0 {
        t.Fatalf("expected positive latency, got %f", result.Latency)
    }
}

func TestPingTimeout(t *testing.T) {
    // Mock server that sleeps longer than the client timeout
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(3 * time.Second)
        w.WriteHeader(http.StatusOK)
    }))
    defer server.Close()

    result := ping(server.URL, 1*time.Second)
    if result.Success {
        t.Fatalf("expected timeout failure, got success")
    }
    if result.Error == "" {
        t.Fatalf("expected an error message for timeout")
    }
}

func TestComputeSummary(t *testing.T) {
    results := []Result{{URL: "a", Success: true, Latency: 100}, {URL: "b", Success: true, Latency: 200}, {URL: "c", Success: false, Error: "boom"}}
    summary := computeSummary(results)
    if summary.Total != 3 {
        t.Fatalf("expected total 3, got %d", summary.Total)
    }
    if summary.Success != 2 {
        t.Fatalf("expected success 2, got %d", summary.Success)
    }
    if summary.Failed != 1 {
        t.Fatalf("expected failed 1, got %d", summary.Failed)
    }
    if summary.MinMs != 100 {
        t.Fatalf("expected min 100, got %f", summary.MinMs)
    }
    if summary.MaxMs != 200 {
        t.Fatalf("expected max 200, got %f", summary.MaxMs)
    }
    if summary.AvgMs != 150 {
        t.Fatalf("expected avg 150, got %f", summary.AvgMs)
    }
    if summary.SurvivalScore != 66 { // 2/3 * 100 = 66 (integer truncation)
        t.Fatalf("expected survival score 66, got %d", summary.SurvivalScore)
    }
}
