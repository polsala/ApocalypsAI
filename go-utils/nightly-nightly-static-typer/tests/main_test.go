package main

import (
    "testing"
)

// containsRune reports whether r is present in slice.
func containsRune(slice []rune, r rune) bool {
    for _, v := range slice {
        if v == r {
            return true
        }
    }
    return false
}

// stripStatic removes any static characters from the string.
func stripStatic(s string) string {
    out := make([]rune, 0, len(s))
    for _, r := range s {
        if !containsRune(staticChars, r) {
            out = append(out, r)
        }
    }
    return string(out)
}

func TestProcessLinesPreservesContent(t *testing.T) {
    input := []string{"hello", "world", "go is fun"}
    workers := 3
    seed := int64(12345) // deterministic seed for reproducibility

    output := processLines(input, workers, seed)
    if len(output) != len(input) {
        t.Fatalf("expected %d output lines, got %d", len(input), len(output))
    }

    for i, line := range output {
        // Verify original characters are still present in order.
        cleaned := stripStatic(line)
        if cleaned != input[i] {
            t.Fatalf("line %d: cleaned output %q does not match original %q", i, cleaned, input[i])
        }
        // Verify length grew by floor(len/5).
        expectedLen := len([]rune(input[i])) + len([]rune(input[i]))/5
        if len([]rune(line)) != expectedLen {
            t.Fatalf("line %d: length %d, expected %d", i, len([]rune(line)), expectedLen)
        }
    }
}
