package main

import "testing"

func TestIndexInBase64(t *testing.T) {
    if idx := indexInBase64('A'); idx != 0 {
        t.Fatalf("expected 0, got %d", idx)
    }
    if idx := indexInBase64('a'); idx != 26 {
        t.Fatalf("expected 26, got %d", idx)
    }
    if idx := indexInBase64('+'); idx != 62 {
        t.Fatalf("expected 62, got %d", idx)
    }
    if idx := indexInBase64('/'); idx != 63 {
        t.Fatalf("expected 63, got %d", idx)
    }
    if idx := indexInBase64('='); idx != -1 {
        t.Fatalf("expected -1 for padding, got %d", idx)
    }
}

func TestColorForChar(t *testing.T) {
    // 'A' maps to index 0 -> colorMap[0] = 31
    if c := colorForChar('A'); c != 31 {
        t.Fatalf("expected color 31, got %d", c)
    }
    // padding character should default to white (37)
    if c := colorForChar('='); c != 37 {
        t.Fatalf("expected default color 37, got %d", c)
    }
}
