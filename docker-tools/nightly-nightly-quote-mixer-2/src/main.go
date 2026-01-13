package main

import (
    "encoding/json"
    "log"
    "math/rand"
    "net/http"
    "time"
)

var inspirational = []string{
    "The early bird catches the worm",
    "A journey of a thousand miles begins with a single step",
    "Fortune favors the bold",
}

var apocalyptic = []string{
    "as the sky cracks open",
    "while the earth trembles",
    "when the shadows swallow the sun",
}

// rng is a package‑level random source; it can be overridden in tests for determinism.
var rng = rand.New(rand.NewSource(time.Now().UnixNano()))

type QuoteResponse struct {
    Quote string `json:"quote"`
}

func mixQuote() string {
    i := rng.Intn(len(inspirational))
    a := rng.Intn(len(apocalyptic))
    return inspirational[i] + " " + apocalyptic[a] + "."
}

func quoteHandler(w http.ResponseWriter, r *http.Request) {
    resp := QuoteResponse{Quote: mixQuote()}
    w.Header().Set(\"Content-Type\", \"application/json\")
    json.NewEncoder(w).Encode(resp)
}

func main() {
    http.HandleFunc(\"/quote\", quoteHandler)
    log.Println(\"Starting server on :8080\")
    log.Fatal(http.ListenAndServe(\":8080\", nil))
}

