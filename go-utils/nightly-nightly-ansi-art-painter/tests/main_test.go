package main

import (
    "math/rand"
    "strings"
    "testing"
)

func TestColorizeDeterministicRepeat(t *testing.T) {
    seed := int64(12345)
    rnd1 := rand.New(rand.NewSource(seed))
    rnd2 := rand.New(rand.NewSource(seed))
    s1 := colorize("Test", rnd1)
    s2 := colorize("Test", rnd2)
    if s1 != s2 {
        t.Fatalf("expected same output for same seed")
    }
}

func TestColorizeResetCount(t *testing.T) {
    rnd := rand.New(rand.NewSource(int64(42)))
    out := colorize("AB", rnd)
    if out == "" {
        t.Fatalf("output is empty")
    }
    count := strings.Count(out, reset)
    if count != 2 {
        t.Fatalf("expected 2 reset codes, got %d", count)
    }
}
