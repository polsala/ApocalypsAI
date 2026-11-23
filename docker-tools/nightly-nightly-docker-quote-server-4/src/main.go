package main

import (
    "encoding/json"
    "log"
    "math/rand"
    "net/http"
    "time"
)

var quotes = []string{
    "The sky fell, but we still have coffee.",
    "When the world ends, make sure your Wi‑Fi is still on.",
    "Apocalypse now? Nah, just a Tuesday.",
    "Survive the fallout, then binge‑watch the after‑show.",
    "Even the zombies need a good playlist.",
}

func getRandomQuote() string {
    return quotes[rand.Intn(len(quotes))]
}

type quoteResponse struct {
    Quote string `json:"quote"`
}

func quoteHandler(w http.ResponseWriter, r *http.Request) {
    resp := quoteResponse{Quote: getRandomQuote()}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func main() {
    rand.Seed(time.Now().UnixNano())
    http.HandleFunc("/", quoteHandler)
    log.Println("Starting server on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
