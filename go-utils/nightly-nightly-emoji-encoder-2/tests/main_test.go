package main

import "testing"

func TestEncodeBasic(t *testing.T) {
    got := encode("abc")
    want := "😀😁😂"
    if got != want {
        t.Fatalf("encode('abc') = %s; want %s", got, want)
    }
}

func TestEncodeMixed(t *testing.T) {
    got := encode("Hello 123")
    // h e l l o space 1 2 3 -> 😆😃😍😍😗⬜1️⃣2️⃣3️⃣
    want := "😆😃😍😍😗⬜1️⃣2️⃣3️⃣"
    if got != want {
        t.Fatalf("encode('Hello 123') = %s; want %s", got, want)
    }
}

func TestEncodeUnknown(t *testing.T) {
    got := encode("@")
    want := "❓"
    if got != want {
        t.Fatalf("encode('@') = %s; want %s", got, want)
    }
}
