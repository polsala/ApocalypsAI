package main

import "testing"

func TestRot13(t *testing.T) {
    cases := []struct {
        in  string
        out string
    }{
        {"Hello, World!", "Uryyb, Jbeyq!"},
        {"Uryyb, Jbeyq!", "Hello, World!"},
        {"Apocalypse", "Ncnpbfvrpr"},
        {"", ""},
    }
    for _, c := range cases {
        got := rot13(c.in)
        if got != c.out {
            t.Fatalf("rot13(%q) = %q; want %q", c.in, got, c.out)
        }
    }
}
