package main

import (
    "bufio"
    "net/http"
    "net/http/httptest"
    "os"
    "testing"
    "time"
)

func TestSSEWeatherEndpoint(t *testing.T) {
    // # Mock rationale: set deterministic seed and enable test mode to avoid time‑based reseeding.
    os.Setenv("TEST_MODE", "1")
    rand.Seed(1)

    // Use a very short interval to make the test fast.
    testInterval := 10 * time.Millisecond
    interval = &testInterval

    server := httptest.NewServer(http.HandlerFunc(sseHandler))
    defer server.Close()

    req, err := http.NewRequest("GET", server.URL+"/weather", nil)
    if err != nil {
        t.Fatalf("failed to create request: %v", err)
    }
    req.Header.Set("Accept", "text/event-stream")

    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        t.Fatalf("request failed: %v", err)
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        t.Fatalf("expected 200 OK, got %d", resp.StatusCode)
    }

    scanner := bufio.NewScanner(resp.Body)
    // Read first few lines; we expect at least an "event:" line followed by a "data:" line.
    var gotEvent, gotData bool
    timeout := time.After(2 * time.Second)
    for !(gotEvent && gotData) {
        select {
        case <-timeout:
            t.Fatalf("timeout waiting for SSE lines")
        default:
            if !scanner.Scan() {
                t.Fatalf("scanner error: %v", scanner.Err())
            }
            line := scanner.Text()
            if line == "event: weather" {
                gotEvent = true
            }
            if len(line) > 5 && line[:5] == "data:" {
                gotData = true
            }
        }
    }
}
