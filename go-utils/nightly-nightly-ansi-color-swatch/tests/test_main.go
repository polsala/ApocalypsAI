package main

import (
    "strings"
    "testing"
)

func TestGenerateSwatchContainsKnownColors(t *testing.T) {
    output := generateSwatch()
    // Check that reset code is present
    if !strings.Contains(output, "\x1b[0m") {
        t.Fatalf("output missing reset escape sequence")
    }
    // Check a few specific color codes
    expected := []string{
        "\x1b[48;5;0m   0 \x1b[0m",
        "\x1b[48;5;255m 255 \x1b[0m",
    }
    for _, exp := range expected {
        if !strings.Contains(output, exp) {
            t.Fatalf("output missing expected segment: %q", exp)
        }
    }
}
