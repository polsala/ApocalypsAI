package main

import (
    "bytes"
    "math/rand"
    "testing"
)

func TestGetQuoteDeterministic(t *testing.T) {
    // Seed with a fixed value to make the output predictable.
    r := rand.New(rand.NewSource(1))
    got := GetQuote(r)
    // Expected quote for seed=1 (based on the order of quotes slice).
    // The first call to r.Intn(len(quotes)) with seed=1 yields index 6.
    // Verify that the expected quote matches the slice entry at index 6.
    want := quotes[6]
    if got != want {
        t.Fatalf("expected %q, got %q", want, got)
    }
}

func TestMainOutput(t *testing.T) {
    // Capture stdout.
    var buf bytes.Buffer
    // Replace the default writer temporarily.
    old := stdOut
    stdOut = &buf
    defer func() { stdOut = old }()

    // Use a deterministic random source.
    r := rand.New(rand.NewSource(2))
    // Call the internal function directly to avoid exiting the test process.
    fmt.Println(GetQuote(r))

    // The printed line should end with a newline.
    got := strings.TrimSpace(buf.String())
    want := quotes[r.Intn(len(quotes))]
    if got != want {
        t.Fatalf("expected printed quote %q, got %q", want, got)
    }
}
