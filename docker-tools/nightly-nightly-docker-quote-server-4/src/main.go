package main

import (
    "encoding/json"
    "log"
    "net/http"
    "os"
    "strconv"
)

var quotes = []string{
    "The sun rises even in the wasteland.",
    "Never trust a silent reactor.",
    "Keep your water filter close and your jokes closer.",
    "Even a broken compass points somewhere.",
    "Hope is the best radiation shield.",
}

type QuoteResponse struct {
    Quote string `json:"quote"`
}

func getQuote(w http.ResponseWriter, r *http.Request) {
    idx := 0
    if val, ok := os.LookupEnv("QUOTE_INDEX"); ok {
        if i, err := strconv.Atoi(val); err == nil && i >= 0 && i < len(quotes) {
            idx = i
        }
    }
    resp := QuoteResponse{Quote: quotes[idx]}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func main() {
    http.HandleFunc("/quote", getQuote)
    port := "8080"
    if p, ok := os.LookupEnv("PORT"); ok {
        port = p
    }
    log.Printf("Starting server on :%s", port)
    if err := http.ListenAndServe(":"+port, nil); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
