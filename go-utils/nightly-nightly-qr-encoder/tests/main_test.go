package main

import "testing"

func TestGenerateQR_ShortString(t *testing.T) {
    // Input length 2 => size = (2 % 4) + 3 = 5
    input := "AB"
    expected := "+-----+\n|*****|\n|*   *|\n|*   *|\n|*   *|\n|*****|\n+-----+"
    got := generateQR(input)
    if got != expected {
        t.Fatalf("unexpected QR output.\nGot:\n%v\nExpected:\n%v", got, expected)
    }
}

func TestGenerateQR_EmptyString(t *testing.T) {
    // Empty input length 0 => size = (0 % 4) + 3 = 3
    input := ""
    expected := "+---+\n|***|\n|***|\n+---+"
    got := generateQR(input)
    if got != expected {
        t.Fatalf("unexpected QR output for empty string.\nGot:\n%v\nExpected:\n%v", got, expected)
    }
}

// Mock rationale: The tests verify the deterministic placeholder algorithm without external dependencies.
