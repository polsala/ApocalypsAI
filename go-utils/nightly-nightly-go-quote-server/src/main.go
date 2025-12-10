package main

import (
    "encoding/json"
    "log"
    "math/rand"
    "net/http"
    "strconv"
    "time"
)

var quotes = []string{
    "The early bird gets the worm, but the second mouse gets the cheese.",
    "When life gives you lemons, make lemonade. Then find someone whose life gave them vodka, and have a party.",
    "I put the ""pro"" in procrastination.",
    "If at first you don't succeed, skydiving is not for you.",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I told my computer I needed a break, and it gave me a coffee break error.",
    "In a world full of copies, be an original error message.",
    "The road to success is always under construction.",
    "Never trust an atom, they make up everything.",
    "To err is human, to debug is divine.",
}

type quoteResponse struct {
    Quote string `json:"quote"`
}

func quoteHandler(w http.ResponseWriter, r *http.Request) {
    // Determine random source – use seed if provided for deterministic output
    var src rand.Source
    if seedStr := r.URL.Query().Get("seed"); seedStr != "" {
        if seed, err := strconv.ParseInt(seedStr, 10, 64); err == nil {
            src = rand.NewSource(seed)
        } else {
            // Invalid seed – fallback to time‑based source
            src = rand.NewSource(time.Now().UnixNano())
        }
    } else {
        src = rand.NewSource(time.Now().UnixNano())
    }
    rnd := rand.New(src)
    idx := rnd.Intn(len(quotes))
    resp := quoteResponse{Quote: quotes[idx]}
    w.Header().Set("Content-Type", "application/json")
    if err := json.NewEncoder(w).Encode(resp); err != nil {
        http.Error(w, "internal server error", http.StatusInternalServerError)
    }
}

func main() {
    http.HandleFunc("/quote", quoteHandler)
    log.Println("Starting quote server on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
