package main

import "testing"

func TestGenerateQRCode(t *testing.T) {
    text := "https://example.com"
    data, err := generateQRCode(text)
    if err != nil {
        t.Fatalf("expected no error, got %v", err)
    }
    if len(data) == 0 {
        t.Fatalf("expected non‑empty QR code data")
    }
    // Verify PNG header bytes
    if string(data[:8]) != "\x89PNG\r\n\x1a\n" {
        t.Fatalf("expected PNG header, got %x", data[:8])
    }
}
