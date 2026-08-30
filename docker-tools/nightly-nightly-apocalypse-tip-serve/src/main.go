package main

import (
    "fmt"
    "log"
    "net/http"
    "os"
    "strconv"
)

var tips = []string{
    "Always keep a spare can opener.",
    "Never trust a silent radio.",
    "Water is more valuable than gold.",
    "Map the stars before night falls.",
    "Scavenge with a purpose.",
}

func handler(w http.ResponseWriter, r *http.Request) {
    seedStr := os.Getenv("SEED")
    idx := 0
    if seedStr != "" {
        if s, err := strconv.Atoi(seedStr); err == nil {
            idx = s % len(tips)
        }
    }
    fmt.Fprintln(w, tips[idx])
}

func main() {
    http.HandleFunc("/", handler)
    log.Println("Starting server on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatal(err)
    }
}
