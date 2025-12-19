package main

import "testing"

func TestPickItemDeterministic(t *testing.T) {
    items := []Item{{Name: "Water", Weight: 5}, {Name: "Canned Food", Weight: 3}, {Name: "First Aid Kit", Weight: 1}, {Name: "Battery Pack", Weight: 1}}
    // Seed 42 is chosen arbitrarily; the expected result was derived by running the algorithm once.
    expected := "Water"
    got, err := pickItem(items, 42)
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if got != expected {
        t.Fatalf("expected %s, got %s", expected, got)
    }
}

func TestPickItemZeroWeight(t *testing.T) {
    items := []Item{{Name: "Nothing", Weight: 0}}
    _, err := pickItem(items, 1)
    if err == nil {
        t.Fatalf("expected error due to zero total weight, got nil")
    }
}
