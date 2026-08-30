package main

import (
    "math/rand"
    "testing"
)

func TestGenerateMessageDeterministic(t *testing.T) {
    seed := int64(42)
    r := rand.New(rand.NewSource(seed))
    got := generateMessage(r)
    expected := "GAMMA: Supply convoy incoming, ETA 0300."
    if got != expected {
        t.Fatalf("expected %q, got %q", expected, got)
    }
}
