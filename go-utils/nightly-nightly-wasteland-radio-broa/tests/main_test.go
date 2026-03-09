package main

import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"
    "time"
)

func TestGenerateSchedule(t *testing.T) {
    fixed := time.Date(2023, 1, 1, 12, 0, 0, 0, time.UTC)
    s := generateSchedule(fixed)
    if len(s) != len(messages) {
        t.Fatalf("expected %d broadcasts, got %d", len(messages), len(s))
    }
    for i, b := range s {
        expected := fixed.Add(time.Duration(i) * time.Minute)
        if !b.Time.Equal(expected) {
            t.Errorf("broadcast %d time mismatch: got %v want %v", i, b.Time, expected)
        }
        if b.Message != messages[i] {
            t.Errorf("broadcast %d message mismatch", i)
        }
    }
}

func TestScheduleHandler(t *testing.T) {
    // Set a deterministic schedule for the test
    fixed := time.Date(2023, 1, 1, 12, 0, 0, 0, time.UTC)
    mu.Lock()
    schedule = generateSchedule(fixed)
    mu.Unlock()

    req := httptest.NewRequest(http.MethodGet, "/schedule", nil)
    w := httptest.NewRecorder()
    scheduleHandler(w, req)

    resp := w.Result()
    defer resp.Body.Close()
    if resp.StatusCode != http.StatusOK {
        t.Fatalf("expected status 200, got %d", resp.StatusCode)
    }

    var got []Broadcast
    if err := json.NewDecoder(resp.Body).Decode(&got); err != nil {
        t.Fatalf("failed to decode response: %v", err)
    }

    if len(got) != len(messages) {
        t.Fatalf("expected %d broadcasts, got %d", len(messages), len(got))
    }
    // Verify first entry matches the fixed start time and message
    if !got[0].Time.Equal(fixed) || got[0].Message != messages[0] {
        t.Errorf("first broadcast mismatch")
    }
}
