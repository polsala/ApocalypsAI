package main

import (
    "fmt"
    "math/rand"
    "time"
)

// Quote represents a quote and its associated emoji.
// It is exported for testing purposes.
// The struct is intentionally simple.
// No external dependencies are required.
// The quotes slice is intentionally small for demonstration.
// Feel free to extend it.

type Quote struct {
    Text  string
    Emoji string
}

var quotes = []Quote{
    {"The only limit to our realization of tomorrow is our doubts of today.", "ð¤"},
    {"Life is 10% what happens to us and 90% how we react to it.", "ðª"},
    {"The best way to predict the future is to create it.", "ð"},
    {"Believe you can and you're halfway there.", "ð"},
}

// pickQuote selects a random quote from the list.
func pickQuote() Quote {
    idx := rand.Intn(len(quotes))
    return quotes[idx]
}

func main() {
    rand.Seed(time.Now().UnixNano())
    q := pickQuote()
    fmt.Printf("%s %s\n", q.Emoji, q.Text)
}

