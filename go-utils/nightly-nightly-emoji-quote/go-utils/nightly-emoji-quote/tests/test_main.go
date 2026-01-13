package main

import (
    "bytes"
    "fmt"
    "math/rand"
    "os"
    "testing"
)

func TestPickQuoteDeterministic(t *testing.T) {
    rand.Seed(1)
    q := pickQuote()
    expected := quotes[1]
    if q != expected {
        t.Fatalf("expected %v, got %v", expected, q)
    }
}

func TestMainOutput(t *testing.T) {
    rand.Seed(1)
    oldStdout := os.Stdout
    r, w, _ := os.Pipe()
    os.Stdout = w

    main()

    w.Close()
    var buf bytes.Buffer
    buf.ReadFrom(r)
    os.Stdout = oldStdout

    got := buf.String()
    expected := fmt.Sprintf("%s %s\n", quotes[1].Emoji, quotes[1].Text)
    if got != expected {
        t.Fatalf("expected %q, got %q", expected, got)
    }
}

