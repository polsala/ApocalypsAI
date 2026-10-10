package main

import "testing"

func TestFormatPingMessage(t *testing.T) {
    got := formatPingMessage(42)
    want := "Ping:42"
    if got != want {
        t.Fatalf("formatPingMessage(42) = %s; want %s", got, want)
    }
}

func TestParsePongMessage_Valid(t *testing.T) {
    seq, err := parsePongMessage("Pong:7")
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if seq != 7 {
        t.Fatalf("expected 7, got %d", seq)
    }
}

func TestParsePongMessage_InvalidPrefix(t *testing.T) {
    _, err := parsePongMessage("Foo:7")
    if err == nil {
        t.Fatalf("expected error for invalid prefix, got nil")
    }
}

func TestParsePongMessage_Malformed(t *testing.T) {
    _, err := parsePongMessage("Pong")
    if err == nil {
        t.Fatalf("expected error for malformed message, got nil")
    }
}
