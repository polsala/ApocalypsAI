package main

import (
    "fmt"
    "log"
    "math/rand"
    "net/http"
    "time"
)

var quotes = []string{
    "The early bird gets the worm, but the second mouse gets the cheese.",
    "When life gives you lemons, make lemonade… and then find someone whose life gave them vodka.",
    "I put the 'pro' in procrastination.",
    "If at first you don't succeed, skydiving is not for you.",
    "Debugging: Being the detective in a crime movie where you are also the murderer.",
}

// getRandomQuote returns a random quote from the quotes slice.
// It is deterministic when the random seed is set.
func getRandomQuote() string {
    if len(quotes) == 0 {
        return ""
    }
    idx := rand.Intn(len(quotes))
    return quotes[idx]
}

// quoteHandler writes a random quote to the response.
func quoteHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, getRandomQuote())
}

func main() {
    rand.Seed(time.Now().UnixNano())
    http.HandleFunc("/", quoteHandler)
    log.Println("Starting server on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
