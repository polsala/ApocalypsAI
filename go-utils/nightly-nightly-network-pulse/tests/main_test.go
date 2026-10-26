package main

import (
    "bytes"
    "encoding/json"
    "io"
    "net/http"
    "net/http/httptest"
    "os"
    "testing"
    "time"
)

func TestPingSuccess(t *testing.T) {
    // Server that responds after a short delay
    srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(10 * time.Millisecond)
        w.WriteHeader(http.StatusOK)
        w.Write([]byte("ok"))
    }))
    defer srv.Close()

    res := ping(srv.URL, 2*time.Second)
    if res.Error != "" {
        t.Fatalf("unexpected error: %s", res.Error)
    }
    if res.StatusCode != http.StatusOK {
        t.Fatalf("expected 200, got %d", res.StatusCode)
    }
    if res.DurationMs < 9 || res.DurationMs > 50 {
        t.Fatalf("unexpected duration %f ms", res.DurationMs)
    }
}

func TestPingTimeout(t *testing.T) {
    // Server that sleeps longer than the timeout
    srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(200 * time.Millisecond)
        w.WriteHeader(http.StatusOK)
    }))
    defer srv.Close()

    res := ping(srv.URL, 50*time.Millisecond)
    if res.Error == "" {
        t.Fatalf("expected timeout error, got none")
    }
}

func TestMainOutput(t *testing.T) {
    // Fast server
    fast := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
    }))
    defer fast.Close()
    // Slow server with different status
    slow := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(30 * time.Millisecond)
        w.WriteHeader(http.StatusTeapot)
    }))
    defer slow.Close()

    // Capture stdout
    oldStdout := os.Stdout
    r, w, _ := os.Pipe()
    os.Stdout = w

    // Simulate command‑line arguments
    os.Args = []string{"cmd", "-timeout", "1", fast.URL, slow.URL}
    main()

    w.Close()
    os.Stdout = oldStdout
    var buf bytes.Buffer
    io.Copy(&buf, r)

    var results []Result
    if err := json.Unmarshal(buf.Bytes(), &results); err != nil {
        t.Fatalf("invalid JSON output: %v", err)
    }
    if len(results) != 2 {
        t.Fatalf("expected 2 results, got %d", len(results))
    }
}
