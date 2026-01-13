package main

import "testing"

func TestEncodeDecode(t *testing.T) {
    original := "Hello, World!"
    encoded := encodeMessage(original)
    decoded := decodeMessage(encoded)
    if decoded != original {
        t.Fatalf("expected %s, got %s", original, decoded)
    }
}

func TestEncodeTrimsWhitespace(t *testing.T) {
    original := "  spaced text  "
    encoded := encodeMessage(original)
    decoded := decodeMessage(encoded)
    expected := "spaced text"
    if decoded != expected {
        t.Fatalf("expected %s, got %s", expected, decoded)
    }
}

