package main

import (
    "encoding/json"
    "log"
    "math/rand"
    "net/http"
    "time"
)

type Quote struct {
    Quote string `json:"quote"`
}

var quotes = []string{
    "Coffee is the gasoline of the soul.",
    "Life begins after coffee.",
    "Espresso yourself!",
    "May your coffee be strong and your code be bug‑free.",
    "When in doubt, add more coffee.",
}

func randomQuote() string {
    rand.Seed(time.Now().UnixNano())
    return quotes[rand.Intn(len(quotes))]
}

func quoteHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodGet {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }
    q := Quote{Quote: randomQuote()}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(q)
}

func main() {
    http.HandleFunc("/quote", quoteHandler)
    log.Println("Starting server on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
