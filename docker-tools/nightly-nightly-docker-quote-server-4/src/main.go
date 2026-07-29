package main

import (
    "encoding/json"
    "log"
    "math/rand"
    "net/http"
    "time"
)

var quotes = []string{
    "The early bird gets the worm, but the second mouse gets the cheese.",
    "When life gives you lemons, make lemonade… and then find someone whose life gave them vodka.",
    "I’m not lazy, I’m on energy‑saving mode.",
    "If at first you don’t succeed, skydiving is not for you.",
    "Adventure is out there… unless you left it at home.",
}

type QuoteResponse struct {
    Quote string `json:"quote"`
}

func quoteHandler(w http.ResponseWriter, r *http.Request) {
    rand.Seed(time.Now().UnixNano())
    q := quotes[rand.Intn(len(quotes))]
    resp := QuoteResponse{Quote: q}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func main() {
    http.HandleFunc("/quote", quoteHandler)
    log.Println("Starting server on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
