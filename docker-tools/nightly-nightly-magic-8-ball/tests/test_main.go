package main

import (
	"testing"
)

func TestAnswerDeterministic(t *testing.T) {
	seed := int64(42)
	got1 := answer("Will it rain tomorrow?", seed)
	got2 := answer("Will it rain tomorrow?", seed)
	if got1 != got2 {
		t.Fatalf("expected same answer for same seed, got %q and %q", got1, got2)
	}
}

func TestAnswerRandom(t *testing.T) {
	// Ensure answer is one of the responses
	question := "Will I win the lottery?"
	got := answer(question, 0)
	found := false
	for _, r := range responses {
		if r == got {
			found = true
			break
		}
	}
	if !found {
		t.Fatalf("got unexpected answer %q", got)
	}
}
