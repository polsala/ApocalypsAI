package main

import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"
    "time"
)

// Mock rationale: replace the real time source with a fixed timestamp for deterministic testing.
func TestNowHandler_WithValidTimezone(t *testing.T) {
    // Fixed point in time: 2025-12-14 15:04:05 UTC
    fixedTime := time.Date(2025, 12, 14, 15, 4, 5, 0, time.UTC)
    getNow = func() time.Time { return fixedTime }
    defer func() { getNow = time.Now }() // restore after test

    req := httptest.NewRequest(http.MethodGet, "/now?tz=America/New_York", nil)
    w := httptest.NewRecorder()
    nowHandler(w, req)

    res := w.Result()
    if res.StatusCode != http.StatusOK {
        t.Fatalf("expected status 200, got %d", res.StatusCode)
    }
    var tr timeResponse
    if err := json.NewDecoder(res.Body).Decode(&tr); err != nil {
        t.Fatalf("failed to decode response: %v", err)
    }
    expectedLoc, _ := time.LoadLocation("America/New_York")
    expectedTime := fixedTime.In(expectedLoc).Format(time.RFC3339)
    if tr.Timezone != "America/New_York" || tr.Time != expectedTime {
        t.Fatalf("unexpected response: got %+v, want timezone=%s time=%s", tr, "America/New_York", expectedTime)
    }
}

func TestNowHandler_WithInvalidTimezone(t *testing.T) {
    req := httptest.NewRequest(http.MethodGet, "/now?tz=Invalid/Zone", nil)
    w := httptest.NewRecorder()
    nowHandler(w, req)

    res := w.Result()
    if res.StatusCode != http.StatusBadRequest {
        t.Fatalf("expected status 400 for invalid timezone, got %d", res.StatusCode)
    }
}

func TestNowHandler_WithoutTimezone(t *testing.T) {
    // Fixed time to make the random selection deterministic via seeding.
    fixedTime := time.Date(2025, 12, 14, 0, 0, 0, 0, time.UTC)
    getNow = func() time.Time { return fixedTime }
    defer func() { getNow = time.Now }()

    // Seed the random generator with a known value to predict the chosen timezone.
    // The randomTimezone function seeds with time.Now().UnixNano(), which we cannot control directly.
    // Instead, we monkey‑patch randomTimezone for the test.
    originalRandom := randomTimezone
    defer func() { randomTimezone = originalRandom }()
    randomTimezone = func() string { return "UTC" }

    req := httptest.NewRequest(http.MethodGet, "/now", nil)
    w := httptest.NewRecorder()
    nowHandler(w, req)

    res := w.Result()
    if res.StatusCode != http.StatusOK {
        t.Fatalf("expected status 200, got %d", res.StatusCode)
    }
    var tr timeResponse
    if err := json.NewDecoder(res.Body).Decode(&tr); err != nil {
        t.Fatalf("failed to decode response: %v", err)
    }
    expectedTime := fixedTime.In(time.UTC).Format(time.RFC3339)
    if tr.Timezone != "UTC" || tr.Time != expectedTime {
        t.Fatalf("unexpected response: got %+v, want timezone=UTC time=%s", tr, expectedTime)
    }
}
