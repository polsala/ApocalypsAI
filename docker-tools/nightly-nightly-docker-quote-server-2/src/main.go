package main

import (
    "fmt"
    "log"
    "math/rand"
    "net/http"
    "time"
)

var quotes = []string{
    "The sun rises, but the shadows linger.",
    "Even in the wasteland, laughter echoes.",
    "Hope is a candle in the endless night.",
    "When the clocks stop, we dance.",
    "Stars whisper secrets to the desert.",
}

func randomQuote() string {
    return quotes[rand.Intn(len(quotes))]
}

func quoteHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, randomQuote())
}

func main() {
    rand.Seed(time.Now().UnixNano())
    http.HandleFunc("/", quoteHandler)
    log.Println("Starting server on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
