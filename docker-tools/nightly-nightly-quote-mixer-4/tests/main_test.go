package main

import (
    "math/rand"
    "testing"
)

func TestGenerateMixedQuoteMock(t *testing.T) {
    // Mock rationale: replace slices with single entries to make output deterministic.
    postApoc = []string{"Apocalypse now."}
    inspirational = []string{"Stay hopeful."}
    r := rand.New(rand.NewSource(0))
    got := generateMixedQuote(r)
    want := "Apocalypse now. Stay hopeful."
    if got != want {
        t.Fatalf("expected %q, got %q", want, got)
    }
}
