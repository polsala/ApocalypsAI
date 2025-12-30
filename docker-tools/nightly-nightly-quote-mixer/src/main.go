package main

import (
    "encoding/json"
    "log"
    "math/rand"
    "net/http"
    "time"
)

var inspirational = []string{
    "Stay hopeful",
    "Believe in yourself",
    "Dream big",
    "Keep moving forward",
    "Embrace the journey",
}

var apocalyptic = []string{
    "but keep your gas mask handy",
    "and watch out for the fallout",
    "while the sky burns",
    "as the world crumbles",
    "when the sirens wail",
}

func mixQuote() string {
    rand.Seed(time.Now().UnixNano())
    i := inspirational[rand.Intn(len(inspirational))]
    a := apocalyptic[rand.Intn(len(apocalyptic))]
    return i + ", " + a + "."
}

type quoteResponse struct {
    Quote string `json:"quote"`
}

func quoteHandler(w http.ResponseWriter, r *http.Request) {
    q := mixQuote()
    resp := quoteResponse{Quote: q}
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
