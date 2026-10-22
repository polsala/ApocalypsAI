package main

import (
    "math"
    "testing"
)

// floatEquals checks whether two floating‑point numbers are equal within a small epsilon.
func floatEquals(a, b, epsilon float64) bool {
    return math.Abs(a-b) <= epsilon
}

func TestComputeRemaining(t *testing.T) {
    tests := []struct {
        initial  float64
        halfLife float64
        days     float64
        want     float64
    }{
        {100, 10, 0, 100},
        {100, 10, 10, 50},
        {100, 10, 20, 25},
        {100, 10, 15, 35.35533905932738},
    }

    for _, tt := range tests {
        got := computeRemaining(tt.initial, tt.halfLife, tt.days)
        if !floatEquals(got, tt.want, 1e-9) {
            t.Errorf("computeRemaining(%v, %v, %v) = %v; want %v", tt.initial, tt.halfLife, tt.days, got, tt.want)
        }
    }
}
