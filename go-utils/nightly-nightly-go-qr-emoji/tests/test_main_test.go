package main

import (
    "strings"
    "testing"
)

// TestGenerateQRCode checks that the output contains both emoji characters
// and that the number of lines equals the height of the bitmap.
func TestGenerateQRCode(t *testing.T) {
    input := "test-string"
    out, err := generateQRCode(input)
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if !strings.Contains(out, "⬛️") {
        t.Fatalf("output does not contain black square emoji")
    }
    if !strings.Contains(out, "⬜️") {
        t.Fatalf("output does not contain white square emoji")
    }
    // Verify line count matches bitmap height.
    qr, _ := qrcode.New(input, qrcode.Medium)
    expectedLines := len(qr.Bitmap())
    actualLines := strings.Count(out, "\n") + 1 // last line has no trailing \n
    if expectedLines != actualLines {
        t.Fatalf("expected %d lines, got %d", expectedLines, actualLines)
    }
}
