package main

import (
    "encoding/json"
    "log"
    "math/rand"
    "net/http"
    "os"
    "strconv"
    "time"
)

var prophecies = []string{
    "The sun will rise in the west.",
    "Rats will inherit the throne.",
    "Silence will echo louder than thunder.",
    "The moon will melt into cheese.",
}

func getProphecy() string {
    seedStr := os.Getenv("FORTUNE_SEED")
    if seedStr != "" {
        if s, err := strconv.ParseInt(seedStr, 10, 64); err == nil {
            idx := int(s) % len(prophecies)
            return prophecies[idx]
        }
    }
    rand.Seed(time.Now().UnixNano())
    return prophecies[rand.Intn(len(prophecies))]
}

func handler(w http.ResponseWriter, r *http.Request) {
    resp := map[string]string{"prophecy": getProphecy()}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func main() {
    http.HandleFunc("/", handler)
    log.Println("Starting server on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
