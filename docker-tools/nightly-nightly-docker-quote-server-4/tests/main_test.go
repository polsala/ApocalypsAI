package main

import (
    "math/rand"
    "testing"
)

func TestGetRandomQuoteDeterministic(t *testing.T) {
    // Mock rationale: set a fixed seed to make the random choice predictable.
    rand.Seed(42)
    got := getRandomQuote()
    expected := "If at first you don't succeed, skydiving is not for you."
    if got != expected {
        t.Fatalf("expected %q, got %q", expected, got)
    }
}
