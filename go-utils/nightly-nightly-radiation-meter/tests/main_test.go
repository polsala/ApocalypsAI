package main

import "testing"

func TestRadiationLevel(t *testing.T) {
    cases := []struct {
        loc      string
        expected int
    }{
        {"Chernobyl", 433},
        {"Safe Haven", 412},
        {"", 0},
    }
    for _, c := range cases {
        got := radiationLevel(c.loc)
        if got != c.expected {
            t.Fatalf("radiationLevel(%q) = %d; want %d", c.loc, got, c.expected)
        }
    }
}
