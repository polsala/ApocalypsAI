package main

import "testing"

func TestEncode(t *testing.T) {
    input := []byte("hello world")
    expected := "aGVsbG8gd29ybGQ="
    got := Encode(input)
    if got != expected {
        t.Fatalf("expected %s, got %s", expected, got)
    }
}
