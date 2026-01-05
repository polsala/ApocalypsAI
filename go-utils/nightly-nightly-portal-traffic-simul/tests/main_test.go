package main

import (
    "testing"
    "time"
)

func TestStats_AddTraveler(t *testing.T) {
    s := NewStats()
    s.AddTraveler(2.0, 100*time.Millisecond)
    s.AddTraveler(1.0, 200*time.Millisecond)

    // wait for the longest traveler to finish
    time.Sleep(250 * time.Millisecond)

    snapshot := s.Snapshot()
    if snapshot["total_travelers"].(int) != 2 {
        t.Fatalf("expected total_travelers 2, got %v", snapshot["total_travelers"])
    }
    if snapshot["active_travelers"].(int) != 0 {
        t.Fatalf("expected active_travelers 0 after durations, got %v", snapshot["active_travelers"])
    }
    avgSpeed := snapshot["average_speed"].(float64)
    if avgSpeed < 1.4 || avgSpeed > 1.6 {
        t.Fatalf("expected average_speed ~1.5, got %v", avgSpeed)
    }
    avgDur := snapshot["average_duration_seconds"].(float64)
    if avgDur < 0.149 || avgDur > 0.151 {
        t.Fatalf("expected average_duration_seconds ~0.15, got %v", avgDur)
    }
}
