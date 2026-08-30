package main

import (
    "math"
    "testing"
)

// approxEqual checks if two floats are equal within a small tolerance.
func approxEqual(a, b, tol float64) bool {
    return math.Abs(a-b) <= tol
}

func TestComputeRemaining_Basic(t *testing.T) {
    // 100 units, half‑life 10, after 10 units -> should be 50.
    got := computeRemaining(100, 10, 10)
    want := 50.0
    if !approxEqual(got, want, 1e-9) {
        t.Fatalf("expected %.9f, got %.9f", want, got)
    }
}

func TestComputeRemaining_MultipleHalfLives(t *testing.T) {
    // After 3 half‑lives, amount should be initial * (0.5)^3 = initial/8.
    got := computeRemaining(80, 5, 15) // 3 half‑lives (15/5)
    want := 10.0
    if !approxEqual(got, want, 1e-9) {
        t.Fatalf("expected %.9f, got %.9f", want, got)
    }
}

func TestComputeRemaining_ZeroElapsed(t *testing.T) {
    got := computeRemaining(42, 7, 0)
    want := 42.0
    if !approxEqual(got, want, 1e-9) {
        t.Fatalf("expected %.9f, got %.9f", want, got)
    }
}

func TestComputeRemaining_InvalidHalfLife(t *testing.T) {
    got := computeRemaining(10, 0, 5)
    want := 0.0 // our implementation returns 0 for non‑positive half‑life.
    if got != want {
        t.Fatalf("expected %.9f, got %.9f", want, got)
    }
}
