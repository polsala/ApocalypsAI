package main

import "testing"

func TestDecodeCaesar(t *testing.T) {
    cases := []struct {
        cipher string
        shift  int
        want   string
    }{
        {"KHOOR ZRUOG", 3, "HELLO WORLD"},
        {"khoor zruog", 3, "hello world"},
        {"Bqqmf!", 1, "Apple!"},
        {"", 5, ""},
    }
    for _, c := range cases {
        got := decodeCaesar(c.cipher, c.shift)
        if got != c.want {
            t.Fatalf("decodeCaesar(%q,%d) = %q; want %q", c.cipher, c.shift, got, c.want)
        }
    }
}

func TestParseLine(t *testing.T) {
    shift, cipher, err := parseLine("SHIFT:4:EXAMPLE")
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if shift != 4 || cipher != "EXAMPLE" {
        t.Fatalf("got shift=%d cipher=%q; want 4 EXAMPLE", shift, cipher)
    }

    // Invalid format
    if _, _, err := parseLine("BADFORMAT"); err == nil {
        t.Fatalf("expected error for bad format")
    }

    // Invalid shift
    if _, _, err := parseLine("SHIFT:abc:XYZ"); err == nil {
        t.Fatalf("expected error for non-numeric shift")
    }
}
