package main

import (
    "fmt"
    "log"
    "math/rand"
    "net/http"
)

var inspirational = []string{
    "Reach for the stars",
    "Believe in yourself",
    "Every day is a gift",
}

var apocalyptic = []string{
    "as the world crumbles",
    "while the sky burns",
    "in the shadow of ruin",
}

func mixQuote() string {
    i := rand.Intn(len(inspirational))
    a := rand.Intn(len(apocalyptic))
    return fmt.Sprintf("%s — %s", inspirational[i], apocalyptic[a])
}

func quoteHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    fmt.Fprintf(w, "{\"quote\":\"%s\"}", mixQuote())
}

func main() {
    // Seed for deterministic behavior in tests; production can override via env if desired
    rand.Seed(1)
    http.HandleFunc("/quote", quoteHandler)
    log.Println("Starting server on :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
