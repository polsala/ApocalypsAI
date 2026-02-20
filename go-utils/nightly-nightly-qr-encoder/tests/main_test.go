package main

import "testing"

func TestEncodeRune(t *testing.T) {
    // 'A' = 65 = 01000001
    got := encodeRune('A')
    want := " #      #"
    if got != want {
        t.Fatalf("encodeRune('A') = %q, want %q", got, want)
    }

    // 'B' = 66 = 01000010
    got = encodeRune('B')
    want = " #    # "
    if got != want {
        t.Fatalf("encodeRune('B') = %q, want %q", got, want)
    }
}
