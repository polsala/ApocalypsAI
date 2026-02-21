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
    "When life gives you lemons, make a lemonade stand on the moon.",
    "I put the 'pro' in procrastination.",
    "If at first you don't succeed, skydiving is not for you.",
    "Debugging: The art of removing bugs you never knew existed.",
}

func randomQuote() string {
    rand.Seed(time.Now().UnixNano())
    return quotes[rand.Intn(len(quotes))]
}

func quoteHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, randomQuote())
}

func main() {
    http.HandleFunc("/", quoteHandler)
    log.Println("Starting server on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
