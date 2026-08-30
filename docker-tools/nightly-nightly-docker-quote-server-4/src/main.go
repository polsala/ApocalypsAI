package main

import (
    "fmt"
    "math/rand"
    "net/http"
    "time"
)

var quotes = []string{
    "The early bird gets the worm, but the second mouse gets the cheese.",
    "When life gives you lemons, make lemonade… and then find someone whose life gave them vodka.",
    "I put the 'pro' in procrastination.",
    "If at first you don't succeed, skydiving is not for you.",
    "Why chase rainbows when you can chase coffee?",
}

func quoteHandler(w http.ResponseWriter, r *http.Request) {
    // Seed with current time for randomness
    rand.Seed(time.Now().UnixNano())
    q := quotes[rand.Intn(len(quotes))]
    fmt.Fprintln(w, q)
}

func main() {
    http.HandleFunc("/", quoteHandler)
    // # Mock rationale: using fixed port 8080 for container exposure
    http.ListenAndServe(":8080", nil)
}
